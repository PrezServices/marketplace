"""Find every agent() call in a Workflow script and read its agentType.

A Python port of tools/agent-tools/workflow-scan.ts in
PrezServices/autonomous-delivery. It tokenizes the JavaScript (strings,
templates with ${} nesting, comments, regular expressions) without running it,
and reports what it can't read rather than guessing: a guard that can't see an
agent() call refuses the script.

scan(source) returns (calls, problems). Each call is a dict with line, prompt
(the source text of the first argument) and agent_type: ("absent",),
("literal", value) or ("unreadable", source text). Each problem is
(line, message).
"""

REGEX_AFTER_WORD = {"return", "typeof", "instanceof", "in", "of", "new", "delete", "void", "throw", "case", "do",
                    "else", "yield", "await"}
DIVISION_AFTER = {")", "]", "}"}
CONTINUES_EXPRESSION = {"+", "-", "*", "/", "%", ".", "?.", "?", "[", "(", "|", "&", "<", ">", "=", ":"}
OPEN, CLOSE = {"(", "[", "{"}, {")", "]", "}"}
DYNAMIC_CODE = {"eval", "Function"}
LINE_ENDS = "\n\r  "


class ScanError(Exception):
    def __init__(self, message, offset):
        super().__init__(message)
        self.offset = offset


class Token:
    __slots__ = ("kind", "text", "start", "end")

    def __init__(self, kind, text, start, end):
        self.kind, self.text, self.start, self.end = kind, text, start, end


def line_at(source, offset):
    return source.count("\n", 0, offset) + 1


def _id_start(ch):
    return ch in "$_" or (ch.isidentifier() and not ch.isdigit())


def _id_part(ch):
    return ch == "$" or (ch + "a").isidentifier() or ch.isdigit() or ch in "‌‍"


def _read_template(source, start):
    i = start
    while i < len(source):
        ch = source[i]
        if ch == "\\":
            i += 2
        elif ch == "`":
            return i + 1, False
        elif ch == "$" and source[i + 1:i + 2] == "{":
            return i + 2, True
        else:
            i += 1
    raise ScanError("a template literal is never closed", start)


def _read_quoted(source, start):
    quote, i = source[start], start + 1
    while i < len(source):
        ch = source[i]
        if ch == "\\":
            i += 2
        elif ch == quote:
            return i + 1
        elif ch == "\n":
            break
        else:
            i += 1
    raise ScanError("a string literal is never closed", start)


def _read_regex(source, start):
    i, in_class = start + 1, False
    while i < len(source):
        ch = source[i]
        if ch == "\n":
            break
        if ch == "\\":
            i += 2
            continue
        if ch == "/" and not in_class:
            i += 1
            while i < len(source) and source[i].isalpha():
                i += 1
            return i
        if ch == "[":
            in_class = True
        if ch == "]":
            in_class = False
        i += 1
    raise ScanError("a regular expression is never closed", start)


def _regex_may_start(previous):
    if previous is None:
        return True
    if previous.kind == "id":
        return previous.text in REGEX_AFTER_WORD
    if previous.kind == "punct":
        return previous.text not in DIVISION_AFTER
    if previous.kind == "tpl":
        return previous.text.endswith("${")
    return False


def tokenize(source):
    tokens, open_interpolations, braces, i = [], [], 0, 0

    def push(kind, end):
        nonlocal i
        tokens.append(Token(kind, source[i:end], i, end))
        i = end

    def push_template(start):
        nonlocal braces
        end, interpolates = _read_template(source, start)
        push("tpl", end)
        if interpolates:
            open_interpolations.append(braces)

    while i < len(source):
        ch, nxt = source[i], source[i + 1:i + 2]
        if ch.isspace():
            i += 1
        elif ch == "/" and nxt == "/":
            ends = [source.find(end, i) for end in LINE_ENDS]
            ends = [end for end in ends if end != -1]
            i = min(ends) if ends else len(source)
        elif ch == "/" and nxt == "*":
            end = source.find("*/", i + 2)
            if end == -1:
                raise ScanError("a block comment is never closed", i)
            i = end + 2
        elif ch in "\"'":
            push("str", _read_quoted(source, i))
        elif ch == "`":
            push_template(i + 1)
        elif ch == "}" and open_interpolations and open_interpolations[-1] == braces:
            open_interpolations.pop()
            push_template(i + 1)
        elif _id_start(ch):
            end = i + 1
            while end < len(source) and _id_part(source[end]):
                end += 1
            push("id", end)
        elif ch.isdigit():
            end = i + 1
            while end < len(source) and (source[end].isalnum() or source[end] in "_."):
                end += 1
            push("num", end)
        elif ch == "\\":
            raise ScanError("a backslash outside a string, a template, a regular expression, or a comment can only "
                            "start an identifier escape such as \\u0061gent, which the guard cannot read.", i)
        elif ch == "/" and _regex_may_start(tokens[-1] if tokens else None):
            push("regex", _read_regex(source, i))
        elif source.startswith("...", i):
            push("punct", i + 3)
        elif ch == "?" and nxt == "." and not source[i + 2:i + 3].isdigit():
            push("punct", i + 2)
        else:
            if ch == "{":
                braces += 1
            if ch == "}":
                braces -= 1
            push("punct", i + 1)
    return tokens


def _depth_change(token):
    if token.kind == "punct":
        return 1 if token.text in OPEN else -1 if token.text in CLOSE else 0
    if token.kind == "tpl":
        return (1 if token.text.endswith("${") else 0) - (1 if token.text.startswith("}") else 0)
    return 0


def _closing_index(tokens, open_index):
    depth = 0
    for index in range(open_index, len(tokens)):
        depth += _depth_change(tokens[index])
        if depth == 0:
            return index
    return -1


def _split_on_commas(tokens):
    parts, depth = [[]], 0
    for token in tokens:
        if depth == 0 and token.kind == "punct" and token.text == ",":
            parts.append([])
        else:
            parts[-1].append(token)
        depth += _depth_change(token)
    return parts


def _text_of(source, tokens):
    return source[tokens[0].start:tokens[-1].end] if tokens else ""


def _plain_literal(token):
    quoted = token.kind == "str" or (token.kind == "tpl" and "${" not in token.text)
    if not quoted:
        return None
    body = token.text[1:-1]
    return None if "\\" in body or (token.kind == "tpl" and "`" in body) else body


def _strings_bound_once_by_const(tokens):
    declared = {}
    for index, token in enumerate(tokens[:-1]):
        name = tokens[index + 1]
        if token.kind == "id" and name.kind == "id" and token.text in ("const", "let", "var", "function", "class"):
            declared[name.text] = declared.get(name.text, 0) + 1
    values = {}
    for index, token in enumerate(tokens):
        name, equals, value, after = (tokens[index + k] if index + k < len(tokens) else None for k in range(1, 5))
        literal = _plain_literal(value) if value is not None else None
        continues = after is not None and after.kind == "punct" and after.text in CONTINUES_EXPRESSION
        if (token.text == "const" and name is not None and name.kind == "id" and equals is not None
                and equals.text == "=" and literal is not None and not continues and declared.get(name.text) == 1):
            values[name.text] = literal
    return values


def _agent_type_of(source, options, constants):
    if not options:
        return ("absent",)
    if options[0].text != "{" or options[-1].text != "}" or _closing_index(options, 0) != len(options) - 1:
        return ("unreadable", _text_of(source, options))
    found = ("absent",)
    for prop in _split_on_commas(options[1:-1]):
        if not prop:
            continue
        key = prop[0]
        colon = prop[1] if len(prop) > 1 else None
        name = _plain_literal(key) if key.kind == "str" else key.text
        not_a_pair = colon is not None and colon.text != ":"
        if key.text in ("...", "[") or name is None or not_a_pair:
            return ("unreadable", _text_of(source, prop))
        if name != "agentType":
            continue
        value = prop[2:] if colon is not None else [key]
        only = value[0] if len(value) == 1 else None
        literal = None if only is None else constants.get(only.text) if only.kind == "id" else _plain_literal(only)
        found = ("unreadable", _text_of(source, prop)) if literal is None else ("literal", literal)
    return found


def _use_of(tokens, index):
    before = tokens[index - 1] if index > 0 else None
    after = tokens[index + 1] if index + 1 < len(tokens) else None
    if after is not None and after.text == ":" and before is not None and before.text in ("{", ","):
        return "key"
    return "call" if after is not None and after.text == "(" else "value"


def scan(source):
    try:
        tokens = tokenize(source)
    except ScanError as error:
        return [], [(line_at(source, error.offset), str(error))]
    constants = _strings_bound_once_by_const(tokens)
    calls, problems = [], []
    for index, token in enumerate(tokens):
        if token.kind != "id" or _use_of(tokens, index) == "key":
            continue
        line = line_at(source, token.start)
        if token.text in DYNAMIC_CODE:
            problems.append((line, f"{token.text} builds code at run time, and the guard cannot read an agent() call inside it."))
        elif token.text == "workflow":
            problems.append((line, "workflow() runs a script that the guard cannot read. Run that script as its own "
                                   "Workflow call, so the guard reads it."))
        elif token.text == "agent":
            if _use_of(tokens, index) == "value":
                problems.append((line, "agent is used as a value, so the guard cannot see how it is called. Call agent(...) directly."))
                continue
            close = _closing_index(tokens, index + 1)
            if close == -1:
                problems.append((line, "the brackets of this agent() call never balance."))
                continue
            parts = _split_on_commas(tokens[index + 2:close])
            prompt, options = parts[0], parts[1] if len(parts) > 1 else None
            calls.append({
                "line": line,
                "prompt": _text_of(source, prompt),
                "agent_type": ("absent",) if options is None else _agent_type_of(source, options, constants),
            })
    return calls, problems
