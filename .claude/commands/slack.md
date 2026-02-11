---
description: Process a Slack export from Raw-Materials/Slack queue
---

Process Slack exports from the queue:

1. List files in `Raw-Materials/Slack/`
2. Identify the OLDEST file by date (ascending order)
3. Read ONLY that single file
4. Process and write the summary
5. Archive the processed export
6. STOP — do not process multiple files

## Configuration

Read `config.yaml` for user identity, team, and communication style.

## Process

Follow the summary process in `Guidelines/slack-summary-process.md`.

## Critical Rule

Base your summary ONLY on information directly present in the Slack export file:
- Do NOT incorporate information from memory files
- Do NOT use previous context or other sources
- Every claim must be supported by specific quotes or evidence from the export

If something seems relevant from memory but isn't in the export, exclude it.

## Focus Areas

Extract insights that aren't captured in meetings or formal documentation:
- Strategic developments
- Technical insights
- Team dynamics
- Process observations
- Emerging patterns
- Cross-team coordination

## Wikilinks

Apply Obsidian wikilinks to the output file per `Guidelines/wikilink-guidelines.md`.

## Output

1. Create summary file as `[YYYYMMDD]-slack-summary.md` in `Curated-Context/Team-Communications/`
2. The date should reflect the date range covered by the export, not today's date
3. Archive the processed export: move from `Raw-Materials/Slack/` to `Archive/Raw-Materials/Slack/`
4. Inform the user to run the command again if there are more files to process
