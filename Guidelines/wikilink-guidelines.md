# Wikilink Guidelines for Curated-Context Files

*Referenced by: `/meeting`, `/doc`, `/slack` commands*

## Purpose

Apply Obsidian-style wikilinks (`[[Target]]`) to Curated-Context output files to improve navigability via backlinks and graph view. Links should add genuine navigation value without cluttering the text.

## What to Link

### Always Link

- **People's names**: First mention in each major section. Use full name for the link target, display name as written.
  - `[[Grand Moff Tarkin|Tarkin]]`, `[[Admiral Piett]]`, `[[General Veers|Veers]]`
- **Teams and groups**: `[[Death Star Engineering]]`, `[[Imperial Naval Operations]]`, `[[Stormtrooper Corps]]`, `[[Imperial Intelligence]]`

### Link When Contextually Useful

- **Vendors and partner companies**: `[[SienarTech]]`, `[[Kuat Drive Yards]]`, `[[BlasTech Industries]]`
- **Long-running projects and platforms**: `[[Death Star II Construction]]`, `[[Stormtrooper Training Programme]]`, `[[Thermal Exhaust Port Remediation]]`
- **Recurring meeting series**: `[[Imperial Briefing]]`, `[[Death Star Status Review]]`, `[[Officers' Weekly]]`

### Do Not Link

- Generic technologies (Kubernetes, AWS, Python, gRPC)
- One-off references unlikely to accumulate useful backlinks
- Jira ticket numbers or temporary identifiers
- Concepts or abstract terms (platform convergence, cost optimisation)

## Linking Rules

1. **First mention only** per major section (H2 heading level). Don't link every occurrence.
2. **Use aliases for natural reading**: `[[Grand Moff Tarkin|Tarkin]]` not `[[Grand Moff Tarkin]]` when the text says 'Tarkin'.
3. **Don't link inside headings or quotes.** Keep headings and direct quotes clean.
4. **Don't link in metadata blocks** (date, participants, duration lines).
5. **Prefer the canonical name** as the link target for consistency:
   - People: Full name (`[[Admiral Piett]]`)
   - Teams: Official name (`[[Death Star Engineering]]` not `[[Lemelisk's team]]`)
   - Vendors: Common name (`[[Kuat Drive Yards]]` not `[[KDY]]`; alias as needed: `[[Kuat Drive Yards|KDY]]`)

## Stub Creation

When a command encounters a wikilink target that does not yet have a corresponding file, **create a stub** in the appropriate directory under `Curated-Context/`.

### Stub Directories

| Category | Directory                   | When to create                                                            |
| -------- | --------------------------- | ------------------------------------------------------------------------- |
| People   | `Curated-Context/People/`   | Any named individual who appears in a meeting, document, or Slack summary |
| Teams    | `Curated-Context/Teams/`    | Teams, groups, supergroups, and organisational units                      |
| Vendors  | `Curated-Context/Vendors/`  | External companies, vendors, and partner organisations                    |
| Projects | `Curated-Context/Projects/` | Long-running projects, platforms, and strategic initiatives               |

### Stub Templates

**People** (`Curated-Context/People/{Full Name}.md`):

```
---
aliases:
  - {short name}
role: {job title}
team: "[[{Team}]]"
email: {email}
manager: "[[{Manager Full Name}]]"
last_updated: {YYYY-MM-DD}
location: {city or remote}
start_date: {YYYY-MM-DD}
---

# {Full Name}

- {1-2 bullet points of key context: what they work on, what they're known for.}
```

**Teams** (`Curated-Context/Teams/{Team Name}.md`):

```
---
aliases: [{alternative names}]
lead: "[[{Lead Name}]]"
group: {parent group}
---

# {Team Name}

{1-2 lines: purpose, scope, relationship to other teams.}

## Members
- [[Person One]]
- [[Person Two]]
```

**Vendors** (`Curated-Context/Vendors/{Vendor Name}.md`):

```
---
aliases: [{alternative names}]
status: {Operational | Terminated | Negotiating | Onboarding}
owner: "[[{Primary owner}]]"
primary_contact: "{vendor account manager or primary contact}"
last_renewal: {YYYY-MM or N/A}
contract_term: {e.g. 12 months, 24 months, or N/A}
---

# {Vendor Name}

{1-2 lines: what they provide, relationship to your team.}
```

**Projects** (`Curated-Context/Projects/{Project Name}.md`):

```
---
aliases: [{alternative names}]
owner_team: "[[{Owning Team}]]"
jira_goal: {PROJ-XX if applicable}
---

# {Project Name}

{1-2 lines: purpose, current state.}
```

### Stub Creation Rules

1. **Create stubs only for entities that are linked** (i.e., appear in the Canonical Names list or are new linkable entities).
2. **Name resolution order — ALWAYS resolve names using the Canonical Names list first.** When a first name or alias appears in source material: (a) Check the Canonical Names list below for a match. If a canonical entry matches, use that entry's full name as the link target. (b) If no canonical match exists, **do not invent or look up a full name**. Prompt the user: 'I'd like to create a link/stub for [first name] ([context, e.g. "mentioned in discussion about training platform"]) but they're not in the canonical list. Can you confirm who this is?' Use only a first-name link (e.g. `[[Vader]]`) in the output file until confirmed.
3. **People stubs must always use full name (first and last).** If the last name is not known or not confidently known from source material, **do not create the stub**. Wait for the user's confirmation per rule 2. Use only a first-name alias link in the output file until the stub is created.
4. **Use your organisation's directory as the primary data source for people stubs** where available. Query for official role, email, location, start date, and org hierarchy. Fall back to asking the user if the person cannot be found.
5. **Keep stubs minimal.** The value is in backlinks, not in duplicating information. 1-2 lines of context maximum at creation time.
6. **Don't overwrite existing stubs.** If a file already exists at the target path, leave it. Stubs accumulate context over time through manual editing; commands should not reset that.
7. **Use YAML frontmatter** for structured metadata (aliases, role, team). This enables Obsidian Dataview queries later if desired.
8. **Add new entities to the Canonical Names list** below when creating their stub, to prevent future inconsistencies.

## Canonical Names Reference

Maintain consistent link targets across all files. When a person or entity can be referred to multiple ways, always use the same target:

**People** (use full name):

- `[[Darth Vader]]` (aliases: Vader, Lord Vader, Anakin)
- `[[Grand Moff Tarkin]]` (aliases: Tarkin, Wilhuff)
- `[[Admiral Piett]]` (aliases: Piett, Firmus)
- `[[General Veers]]` (aliases: Veers, Maximilian)
- `[[Moff Jerjerrod]]` (aliases: Jerjerrod, Tiaan)
- `[[Captain Needa]]` (aliases: Needa)
- `[[Colonel Yularen]]` (aliases: Yularen, Wullf)
- `[[Dr. Bevel Lemelisk]]` (aliases: Lemelisk, Bevel)
- `[[TK-421]]` (aliases: TK)

**Teams/Groups**:

- `[[Death Star Operations]]`
- `[[Death Star Engineering]]`
- `[[Imperial Naval Operations]]`
- `[[Stormtrooper Corps]]`
- `[[Imperial Intelligence]]`

**Vendors**:

- `[[SienarTech]]` (aliases: Sienar Fleet Systems)
- `[[Kuat Drive Yards]]` (aliases: KDY)
- `[[BlasTech Industries]]` (aliases: BlasTech)

**Projects**:

- `[[Death Star II Construction]]`
- `[[Stormtrooper Training Programme]]` (aliases: Accuracy Improvement Initiative)
- `[[Thermal Exhaust Port Remediation]]` (aliases: Port Remediation)
- `[[Hoth Assault Planning]]`

## Scope

- **Apply to**: All new Curated-Context output files (meeting summaries, document summaries, Slack summaries)
- **Stub creation**: During output file generation, when a new linkable entity is encountered
- **Do not apply to**: Memory files (`Memory/*.md`), guidelines, command files, raw materials
- **Retroactive linking**: Not required. Link older files opportunistically when revisiting them.
