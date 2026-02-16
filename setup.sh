#!/usr/bin/env bash
# =============================================================================
# AI Context System — Setup Script
# =============================================================================
# Run this once after cloning to get everything in place.
# Safe to re-run — it won't overwrite existing files.
#
# Usage:
#   ./setup.sh            Normal setup (safe to re-run)
#   ./setup.sh --clear    Remove all demo/user data and start fresh
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
skip()    { echo -e "${DIM}  ┊${RESET} $1"; }
header()  { echo -e "\n${BOLD}$1${RESET}"; }

# --- Ensure we're in the project root ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# --- Standard directory structure ---
# These are the canonical directories the system expects.
# Used by both setup and --clear to ensure a clean slate.
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

# =============================================================================
# --clear: Remove all demo/user data and start fresh
# =============================================================================

clear_data() {
    echo ""
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}  AI Context System — Clear Data${RESET}"
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""
    echo -e "  This will ${RED}permanently delete${RESET} all content from:"
    echo ""
    echo -e "    ${RED}•${RESET} Memory/                (system memory files)"
    echo -e "    ${RED}•${RESET} Curated-Context/       (processed insights, people, projects, etc.)"
    echo -e "    ${RED}•${RESET} Raw-Materials/          (transcripts, docs, Slack exports)"
    echo -e "    ${RED}•${RESET} Synced-Data/            (calendar, Jira, news syncs)"
    echo -e "    ${RED}•${RESET} Archive/                (archived content)"
    echo -e "    ${RED}•${RESET} config.yaml             (your personal configuration)"
    echo ""
    echo -e "  ${DIM}System files are preserved: Guidelines/, Prompts/, Scripts/,${RESET}"
    echo -e "  ${DIM}.claude/commands/, Templates/, and config.example.yaml.${RESET}"
    echo ""

    # --- Confirmation ---
    read -rp "  Type 'clear' to confirm: " confirm
    echo ""

    if [ "$confirm" != "clear" ]; then
        echo -e "  ${YELLOW}Cancelled.${RESET} No files were deleted."
        echo ""
        exit 0
    fi

    # --- Count what we're about to remove ---
    removed=0

    # Helper: remove all files in a directory (recursively), report count
    # Usage: clear_dir "Directory/Path" "description"
    clear_dir() {
        local dir="$1"
        local desc="$2"
        local count=0

        if [ ! -d "$dir" ]; then
            skip "No ${desc} directory — skipping"
            return
        fi

        # Find and remove all regular files (not .gitkeep, not directories)
        # Directory structure is left intact — only content files are removed.
        while IFS= read -r -d '' file; do
            rm "$file"
            count=$((count + 1))
        done < <(find "$dir" -type f -not -name '.gitkeep' -print0 2>/dev/null)

        if [ "$count" -gt 0 ]; then
            success "Removed ${count} files from ${desc}"
            removed=$((removed + count))
        else
            skip "No files in ${desc}"
        fi
    }

    header "Clearing data"

    clear_dir "Memory"           "Memory"
    clear_dir "Curated-Context"  "Curated-Context"
    clear_dir "Raw-Materials"    "Raw-Materials"
    clear_dir "Synced-Data"      "Synced-Data"
    clear_dir "Archive"          "Archive"

    # --- Remove config.yaml ---
    if [ -f config.yaml ]; then
        rm config.yaml
        success "Removed config.yaml"
        removed=$((removed + 1))
    else
        skip "No config.yaml to remove"
    fi

    # --- Recreate standard directory structure ---
    header "Recreating directory structure"

    created=0
    for dir in "${DIRS[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            created=$((created + 1))
        fi
    done

    if [ "$created" -gt 0 ]; then
        success "Recreated ${created} directories"
    else
        success "All standard directories intact"
    fi

    # --- Summary ---
    header "Done!"
    echo ""
    if [ "$removed" -gt 0 ]; then
        echo -e "  ${GREEN}Cleared ${removed} files. The system is ready for a fresh start.${RESET}"
    else
        echo -e "  ${GREEN}Nothing to clear — the system was already empty.${RESET}"
    fi
    echo ""
    echo -e "  ${DIM}Next steps:${RESET}"
    echo -e "  ${CYAN}1.${RESET} Run ${BOLD}./setup.sh${RESET} to create a fresh config.yaml"
    echo -e "  ${CYAN}2.${RESET} Edit ${BOLD}config.yaml${RESET} with your real details"
    echo -e "  ${CYAN}3.${RESET} Drop your first transcript into ${BOLD}Raw-Materials/Meeting-Transcripts/${RESET}"
    echo -e "  ${CYAN}4.${RESET} Run ${BOLD}/meeting${RESET} in Claude Code to process it"
    echo ""
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""
}

# --- Handle arguments ---
if [ $# -gt 0 ]; then
    case "$1" in
        --clear)
            clear_data
            exit 0
            ;;
        *)
            echo ""
            echo -e "${BOLD}AI Context System — Setup${RESET}"
            echo ""
            echo -e "Usage: ${CYAN}./setup.sh${RESET}              Run setup (safe to re-run)"
            echo -e "       ${CYAN}./setup.sh --clear${RESET}      Remove all demo/user data and start fresh"
            echo ""
            echo -e "${RED}Unknown option:${RESET} $1"
            echo ""
            exit 1
            ;;
    esac
fi

# =============================================================================
# Normal setup
# =============================================================================

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

created=0
for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        created=$((created + 1))
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
        made_executable=$((made_executable + 1))
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
echo -e "  ${DIM}Tip: Run ${BOLD}./setup.sh --clear${DIM} to remove all demo/user data and start fresh.${RESET}"
echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""
