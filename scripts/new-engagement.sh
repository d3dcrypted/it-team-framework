#!/bin/bash
# new-engagement.sh — Start a new IT Team Framework engagement
# Usage: ./scripts/new-engagement.sh "Company Name" [--size N] [--sector manufacturing] [--stack "..."] [--stdout]
#
# Creates a preconfigured Hermes session with the orchestrator skill
# and pre-filled initial context.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
    echo "Usage: $0 \"Company Name\" [options]"
    echo ""
    echo "Options:"
    echo "  --size N           Number of employees (default: asked during intake)"
    echo "  --sector SECTOR    Industry sector"
    echo "    (manufacturing|logistics|finance|healthcare|services|retail|pa|other)"
    echo "  --stack \"...\"      Current IT stack (free text)"
    echo "  --stdout           Print the prompt instead of starting hermes chat"
    echo "  -h, --help         This help"
    echo ""
    echo "Examples:"
    echo "  $0 \"TechSrl\" --size 50 --sector manufacturing"
    echo "  $0 \"LogisticsInc\" --size 200 --sector logistics --stack \"VMware vSphere, AD, O365, SAP\""
    echo ""
    exit 0
}

# Default values
COMPANY=""
SIZE=""
SECTOR=""
STACK=""
STDOUT=false

# Argument parsing
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help) usage ;;
        --size) SIZE="$2"; shift 2 ;;
        --sector) SECTOR="$2"; shift 2 ;;
        --stack) STACK="$2"; shift 2 ;;
        --stdout) STDOUT=true; shift ;;
        -*|--*) echo "Unknown option: $1"; usage ;;
        *) COMPANY="$1"; shift ;;
    esac
done

if [ -z "$COMPANY" ]; then
    echo "Error: specify the company name"
    usage
fi

# Sector mapping to English labels
case "$SECTOR" in
    manufacturing) SECTOR_EN="Manufacturing/Production" ;;
    logistics) SECTOR_EN="Logistics/Transportation" ;;
    finance) SECTOR_EN="Finance/Banking/Insurance" ;;
    healthcare) SECTOR_EN="Healthcare" ;;
    services) SECTOR_EN="Services/Consulting" ;;
    retail) SECTOR_EN="Retail/Commerce" ;;
    pa) SECTOR_EN="Public Administration" ;;
    other|"") SECTOR_EN="[specify sector]" ;;
    *) SECTOR_EN="$SECTOR" ;;
esac

# Build the initial prompt
PROMPT="New IT Team Framework engagement.

Load skill: it-team-orchestrator

PHASE 0 — COMPANY INTAKE

Company name: ${COMPANY}
Sector: ${SECTOR_EN}"

if [ -n "$SIZE" ]; then
    PROMPT="${PROMPT}
Employees: ${SIZE}"
fi

if [ -n "$STACK" ]; then
    PROMPT="${PROMPT}
Current IT stack: ${STACK}"
fi

PROMPT="${PROMPT}

Proceed with Phase 0 (Intake) by gathering any missing data, then Phase 1 (Parallel Assessment) with all 9 specialists, Phase 2 (Gate Review with it-team-gatekeeper), Phase 3 (Gap Analysis), Phase 4 (Roadmap) and present me the results. Do not execute automatically — present the roadmap to me first for approval."

if [ "$STDOUT" = true ]; then
    echo "=== Prompt for Hermes ==="
    echo ""
    echo "$PROMPT"
else
    # Start hermes chat with the prompt
    echo "🚀 Starting engagement for ${COMPANY}..."
    echo ""
    echo "hermes chat --eval \"\$PROMPT\""
    hermes chat --eval "$PROMPT"
fi