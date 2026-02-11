#!/usr/bin/env bash
# =============================================================================
# AI Context System — Setup Script
# =============================================================================
# Run this once after cloning to get everything in place.
# Safe to re-run — it won't overwrite existing files.
# =============================================================================

set -euo pipefail

# --- Colours (if terminal supports them) ---
if [ -t 1 ]; then
    BOLD='\033[1m'
    DIM='\033[2m'
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    CYAN='\033[0;36m'
    RESET='\033[0m'
else
    BOLD='' DIM='' RED='' GREEN='' YELLOW='' CYAN='' RESET=''
fi

info()    { echo -e "${CYAN}▸${RESET} $1"; }
success() { echo -e "${GREEN}✓${RESET} $1"; }
warn()    { echo -e "${YELLOW}⚠${RESET} $1"; }
header()  { echo -e "\n${BOLD}$1${RESET}"; }

# --- Ensure we're in the project root ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${BOLD}  AI Context System — Setup${RESET}"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

# --- 1. Configuration ---
header "Configuration"

if [ -f config.yaml ]; then
    success "config.yaml already exists — skipping"
else
    cp config.example.yaml config.yaml
    success "Created config.yaml from config.example.yaml"
    warn "Edit config.yaml to replace the Star Wars demo with your details"
fi

# --- 2. Directories ---
header "Directories"

# These directories might not exist if .gitkeep files were removed
# or if the user is setting up from a minimal clone
DIRS=(
    ".claude/commands"
    "Raw-Materials/Meeting-Transcripts"
    "Raw-Materials/Docs"
    "Raw-Materials/Slack"
    "Curated-Context/Daily-Journals"
    "Curated-Context/Delivery-Reports"
    "Curated-Context/Professional-Development"
    "Curated-Context/Interview-Context"
    "Curated-Context/News-Digests"
    "Curated-Context/Organizational-Context"
    "Curated-Context/People"
    "Curated-Context/Professional-Philosophies"
    "Curated-Context/Project-Insights"
    "Curated-Context/Projects"
    "Curated-Context/Strategic-Documents"
    "Curated-Context/Team-Knowledge"
    "Curated-Context/Teams"
    "Curated-Context/Technical-Documentation"
    "Curated-Context/Vendors"
    "Curated-Context/Obsidian-Specific-Dirs/Templates"
    "Memory"
    "Synced-Data/Calendar"
    "Synced-Data/Jira"
    "Synced-Data/News"
    "Prompts"
    "Scripts/News"
    "Sync"
    "Guidelines"
    "Archive/Curated-Context"
    "Archive/Memory"
    "Archive/Guidelines"
    "Archive/Raw-Materials"
)

created=0
for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        ((created++))
    fi
done

if [ "$created" -gt 0 ]; then
    success "Created $created missing directories"
else
    success "All directories present"
fi

# --- 3. Script permissions ---
header "Permissions"

made_executable=0
for script in Scripts/*.py Scripts/**/*.py Sync/*.py setup.sh; do
    if [ -f "$script" ] && [ ! -x "$script" ]; then
        chmod +x "$script"
        ((made_executable++))
    fi
done 2>/dev/null  # suppress glob expansion errors if no matches

if [ "$made_executable" -gt 0 ]; then
    success "Made $made_executable scripts executable"
else
    success "Script permissions OK"
fi

# --- 4. Summary ---
header "Done!"
echo ""
echo -e "  ${GREEN}The AI Context System is ready.${RESET}"
echo ""

if [ ! -f config.yaml ]; then
    echo -e "  ${DIM}Next steps:${RESET}"
    echo -e "  ${CYAN}1.${RESET} Edit ${BOLD}config.yaml${RESET} with your details (or keep the Star Wars demo)"
    echo -e "  ${CYAN}2.${RESET} Drop a meeting transcript into ${BOLD}Raw-Materials/Meeting-Transcripts/${RESET}"
    echo -e "  ${CYAN}3.${RESET} Run ${BOLD}/meeting${RESET} in Claude Code to process it"
    echo -e "  ${CYAN}4.${RESET} Run ${BOLD}/help${RESET} to see all available commands"
else
    echo -e "  ${DIM}Existing memory detected. You're all set.${RESET}"
    echo -e "  Run ${BOLD}/help${RESET} to see available commands."
fi

echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""
