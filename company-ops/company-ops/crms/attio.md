# Attio

Through the Attio MCP server (`https://mcp.attio.com/mcp`). Tool names
change between server versions, so load the schemas once per session
(ToolSearch for `attio`) and use the names the schema shows. The capability
names below are stable.

The config (`.company-ops/config.md`) gives the **workspace**, the **default
owner** and the real name of each stage.

## Kinds

| Kind | In Attio |
| --- | --- |
| person | A `people` record. Its company is the `company` attribute |
| company | A `companies` record, matched by `domains` |
| deal | A `deals` record, with `associated_people`, `associated_company`, `owner`, `value` and `stage` |
| pipeline | Two attributes. Before a deal exists, `people.lead_status` (a select). Once a deal exists, `deals.stage` (a status). The stage table in the config maps each logical stage to one of them |
| touch | A note on the person, and the same note on the deal when there is one |
| owner | A workspace member, resolved by email |

Logical stages span the two attributes like this in a workspace with
Attio's default deal stages. The config's table holds the real names; this
is what setup writes when the names match.

| Logical stage | Attribute | Value |
| --- | --- | --- |
| `lead` | `people.lead_status` | New |
| `contacted` | `people.lead_status` | Contacted |
| `qualified` | `deals.stage` | Qualified |
| `proposal` | `deals.stage` | Proposal |
| `won` | `deals.stage` | Won 🎉 |
| `lost` | `deals.stage` | Lost |

A deal is open when its stage is neither the `won` nor the `lost` value.

## One-time setup

Deals have no next-step date by default. The log operation needs one, so
the first time this adapter runs in a workspace, check
`list-attribute-definitions` on `deals` for `next_step_at`. When it is
missing, propose this change and run it on the user's yes through the
data-model tool:

```
create-attribute on deals: api_slug next_step_at, title "Next step at",
type date, description "Date of the next action on this deal, as the last
touch note's Next line says."
```

The tool asks for workspace admin. When the session cannot run it, give the
user the change to make in Attio's settings and stop.

## Operations

**Find a person.** In this order, stopping at the first key the request
gives: `email_addresses` with `search-records` on `people`; `whatsapp_id`,
then `instagram_id`, with `list-records` on `people` and an `eq` filter
(`search-records` does not index custom text attributes); then full name
with `search-records`, kept only when the company also matches. Never
`phone_numbers` alone: the attribute is not unique. Two or more results
stop the operation and show them.

**Find a company.** `search-records` on `companies` by domain, then by
name. Two or more results stop the operation and show them.

**Upsert a person.** `upsert-record` on `people` with `matching_attribute`
`email_addresses` (or `whatsapp_id` or `instagram_id` when that is the key
the request gives). Values: `name` as `{first_name, last_name, full_name}`,
`company` as the company's record id, `lead_source` and `met_at` when the
request says, `met_by` as the owner's email. Without a unique key, use
`create-record` after a find that returned nothing.

**Upsert a company.** `upsert-record` on `companies` with
`matching_attribute` `domains`. Without a domain, `create-record` after a
find that returned nothing, with `name` only.

**Create a deal.** `create-record` on `deals` with `name` ("<Company> –
<what>"), `stage` (the config's value for the lowest mapped logical stage,
`qualified` in a default workspace), `owner` (email), `value` (a number in
the attribute's currency, CLP here), `associated_company` and
`associated_people` as record references by id.

**Log a touch.** `create-note` on the person (`parent_object` `people`) with
`title` set to the note's first line and `content` to the whole note. The
same call on the deal when one is open. Then `update-record` on the deal
with `next_step_at` set to the Next line's date, or left as is when the line
says "none". When the touch was inbound, also set `last_inbound_at` and
`last_channel` on the person, so the WhatsApp reply window reads right.

**Move a deal.** `update-record` on `deals` with `stage` set to the config's
value. A logical stage mapped to `people.lead_status` moves the person
instead, with `update-record` on `people`.

**Add to pipeline.** Create a deal, as above.

**Review.** Pipeline: `list-records` on `deals` with the filter
`stage neq <won value> and stage neq <lost value>`, up to 50 per page, then
one `search-notes-by-metadata` per deal with `limit` 1 for the last touch
date. People: `list-records` on `people` sorted by `last_inbound_at`
descending, then the same note lookup. Build the table in the reply from
these; `render-record` shows one record as a card when the user asks for
one.

**Resolve the owner.** `list-workspace-members` with the email as `query`.
Pass the email itself in `owner` and `met_by` values; Attio resolves it.

## Traps

- **Phone numbers are not unique.** `people.phone_numbers` is multiselect
  and not unique, so a phone never identifies a person on its own. The
  unique keys are `email_addresses`, `whatsapp_id` and `instagram_id`.
- **Full-text search skips custom attributes.** `search-records` indexes
  domains, emails, phones, names, descriptions, social handles and
  locations. `whatsapp_id` and `instagram_id` are found only with
  `list-records` and an `eq` filter.
- **The data model is read-only from the MCP, except additions.** The MCP
  creates attributes and objects but cannot edit an existing attribute, a
  deal stage, a currency or an activity type. Those go through Attio's
  settings in the browser. Say so instead of retrying.
- **Messages are notes.** Channel messages are logged as notes on the
  record, never as Attio activities or interactions, which the API does not
  write.
- **Ids are UUIDs.** Every mutation takes `record_id`. Get it from a find,
  never from a name.
- **Required deal fields.** `name`, `stage` and `owner` are required on
  `deals`; a create without all three fails.
- **Won carries an emoji.** The default won stage is `Won 🎉`, emoji
  included. Copy the config's value exactly.
