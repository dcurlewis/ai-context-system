---
description: Process a document from Raw-Materials/Docs queue
---

Process documents from the queue:

1. List files in `Raw-Materials/Docs/`
2. Identify the OLDEST file by date (ascending order)
3. Read ONLY that single file
4. Process and write the summary
5. Archive the processed document
6. STOP — do not process multiple files

## Configuration

Read `config.yaml` for user identity, team, and communication style.

## Context Integration

Before summarising, scan recent documents and meeting summaries from past 2 weeks in `Curated-Context/` for:
- Related documents or discussions on this topic
- Previous versions or updates to this content
- Dependencies or impacts on other workstreams

## Balanced Reporting

- **Foundation**: Report what is explicitly stated in the document
- **Context enrichment**: Note connections to recent work where relevant
- **Professional analysis**: Identify implications without dramatisation
- **NO dramatic descriptors** (crisis, critical, urgent) unless directly quoted
- **Attribute all assessments** to document or named authors: "The report describes this as urgent" NOT "This is urgent"

## Summary Structure

1. **Document Overview** — Type, author, date, purpose if stated
2. **Key Topics Covered** — Factual list of what was discussed
3. **Main Findings/Conclusions** — Only those explicitly stated
4. **Action Items** — Items requiring follow-up if mentioned
5. **Key Data Points** — Important metrics, dates, numbers if present
6. **Direct Quotes** — Include 2-3 relevant direct quotes that capture key insights
7. **Context Notes** — Connections to recent work or decisions (if relevant)
8. **Insights** — Professional observations about implications (1-2 max, grounded in facts)

## Wikilinks

Apply Obsidian wikilinks to the output file per `Guidelines/wikilink-guidelines.md`.

## Output

1. Create summary file in appropriate `Curated-Context/` subdirectory using naming format `[YYYYMMDD]-Document-Title.md`:
   - Strategy docs → `Curated-Context/Strategic-Documents/`
   - Technical specs → `Curated-Context/Technical-Documentation/`
   - Project docs → `Curated-Context/Project-Insights/`
   - Org/team docs → `Curated-Context/Organizational-Context/`

2. Archive the processed document: move from `Raw-Materials/Docs/` to `Archive/Raw-Materials/Docs/`

3. Inform the user to run the command again if there are more files to process
