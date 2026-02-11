# Contributing to AI Context System

Thanks for considering a contribution! This project is a personal knowledge management system powered by Claude Code and Claude Desktop, and there's plenty of room to make it better.

---

## Ways to Contribute

### New Slash Commands
The system ships with 24 commands in `.claude/commands/`. If you've built a workflow that others would find useful, we'd love to see it.

**Guidelines for new commands:**
- One file per command in `.claude/commands/`
- Read `config.yaml` for all user-specific information — never hardcode
- Use `[[wikilinks]]` in all generated output
- Follow the existing file naming conventions
- Include clear instructions, a processing template, and memory update guidance
- Test with the Star Wars demo persona before submitting

### Improved Processing Guidelines
Guidelines in `Guidelines/` govern how information is processed. Improvements to consolidation logic, wikilink conventions, or output templates are welcome.

### Sync Connectors
The system currently supports Jira and Google Calendar. Connectors for other tools would be valuable:
- Linear
- Notion
- Google Docs
- Confluence
- Microsoft Teams / Outlook

### Memory System Improvements
The memory pipeline is the core of the system. Ideas for better consolidation, retrieval, or organisation are particularly welcome.

### Documentation
Better docs, more examples, clearer setup instructions — always appreciated.

---

## Development Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-context-system.git
cd ai-context-system

# Run setup
./setup.sh

# The Star Wars demo persona is ready to use — no additional config needed
```

---

## Submitting Changes

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-command`)
3. Make your changes
4. Commit with a clear message
5. Open a pull request

### Commit Messages

Use clear, descriptive commit messages:
- `Add /retrospective command for sprint retrospective processing`
- `Improve memory consolidation to handle cross-file deduplication`
- `Fix wikilink generation for hyphenated project names`

### Code Style

- **Shell scripts**: Use `set -euo pipefail`, quote variables, use functions
- **Python**: Follow PEP 8, include docstrings, type hints appreciated
- **Markdown**: ATX-style headers (`#`), consistent indentation, wikilinks for named entities

---

## Before Submitting

- Don't include real names, company names, or personal information
- Use the Star Wars demo persona for all examples

---

## Questions?

Open an issue! Whether it's a bug report, feature request, or question about how something works, issues are the best way to start a conversation.
