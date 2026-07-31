#!/bin/bash
# deploy-skills.sh — Install all IT Team Framework skills in Hermes
# Usage: ./scripts/deploy-skills.sh
# Requires: hermes CLI available and configured

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HERE="${SCRIPT_DIR}"

echo "=== IT Team Framework — Deploy Skills ==="
echo "Source: ${HERE}"
echo ""

# Map: skill name → SKILL.md path
declare -A SKILLS
SKILLS[it-team-orchestrator]="${HERE}/orchestrator/SKILL.md"
SKILLS[it-team-gatekeeper]="${HERE}/gatekeeper/SKILL.md"
SKILLS[it-team-os-infra]="${HERE}/specialists/os-infra/SKILL.md"
SKILLS[it-team-cloud]="${HERE}/specialists/cloud/SKILL.md"
SKILLS[it-team-applications]="${HERE}/specialists/applications/SKILL.md"
SKILLS[it-team-security]="${HERE}/specialists/security/SKILL.md"
SKILLS[it-team-network]="${HERE}/specialists/network/SKILL.md"
SKILLS[it-team-data]="${HERE}/specialists/data/SKILL.md"
SKILLS[it-team-budget]="${HERE}/specialists/budget/SKILL.md"
SKILLS[it-team-endpoints]="${HERE}/specialists/endpoints/SKILL.md"
SKILLS[it-team-service-desk]="${HERE}/specialists/service-desk/SKILL.md"
SKILLS[it-team-assessment-guide]="${HERE}/assessment/interview-guide.md"

COUNT=0
FAIL=0

for NAME in "${!SKILLS[@]}"; do
    PATH_FILE="${SKILLS[$NAME]}"
    if [ ! -f "$PATH_FILE" ]; then
        echo "⚠️  SKIP: ${NAME} — file not found: ${PATH_FILE}"
        continue
    fi

    echo -n "→ ${NAME} ... "

    # Try to create/update the skill
    if hermes skill create --name "${NAME}" --content "${PATH_FILE}" 2>/dev/null; then
        echo "✅ created"
    elif hermes skill view "${NAME}" >/dev/null 2>&1; then
        # Already exists — update via skill_manage (from within Hermes)
        # For CLI, try using skill update command if available
        if hermes skill update --name "${NAME}" --content "${PATH_FILE}" 2>/dev/null; then
            echo "✅ updated"
        else
            echo "⚠️  exists (use /skill ${NAME} to load it)"
        fi
    else
        echo "❌ failed — create manually with:"
        echo "   hermes skill create --name ${NAME} --content \"${PATH_FILE}\""
        FAIL=$((FAIL + 1))
    fi
    COUNT=$((COUNT + 1))
done

echo ""
echo "=== Summary ==="
echo "Installed: ${COUNT}"
echo "Failed: ${FAIL}"
echo ""
echo "To use: start hermes chat and load the orchestrator skill:"
echo "  /skill it-team-orchestrator"
echo "Then describe your company context."