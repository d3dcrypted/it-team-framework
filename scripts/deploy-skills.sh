#!/bin/bash
# deploy-skills.sh — Sync IT Team Framework skills into Hermes (repo = single source of truth)
# Usage:
#   ./scripts/deploy-skills.sh            # filesystem sync (default): copy repo SKILL.md -> ~/.hermes/skills/it-team/
#   ./scripts/deploy-skills.sh --check    # dry-run: show which installed skills differ from the repo
#   ./scripts/deploy-skills.sh --cli      # legacy mode: install via `hermes skill create/update`
#
# v0.3: the repo is canonical. Installed copies under ~/.hermes/skills/ are build
# artifacts of this script — never edit them directly (they get overwritten).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HERE="${SCRIPT_DIR}"
DEST="${HERMES_SKILLS_DIR:-$HOME/.hermes/skills/it-team}"
DISABLED="${HERMES_DISABLED_DIR:-$HOME/.hermes/disabled-skills}"
MODE="${1:---fs}"

# Map: skill name -> source file (skill name == installed dir name, always)
declare -A SKILLS
SKILLS[it-team-orchestrator]="${HERE}/orchestrator/SKILL.md"
SKILLS[it-team-gatekeeper]="${HERE}/gatekeeper/SKILL.md"
SKILLS[it-team-validator]="${HERE}/validator/SKILL.md"
SKILLS[it-team-os-infra]="${HERE}/specialists/os-infra/SKILL.md"
SKILLS[it-team-cloud]="${HERE}/specialists/cloud/SKILL.md"
SKILLS[it-team-applications]="${HERE}/specialists/applications/SKILL.md"
SKILLS[it-team-security]="${HERE}/specialists/security/SKILL.md"
SKILLS[it-team-network]="${HERE}/specialists/network/SKILL.md"
SKILLS[it-team-data]="${HERE}/specialists/data/SKILL.md"
SKILLS[it-team-budget]="${HERE}/specialists/budget/SKILL.md"
SKILLS[it-team-endpoints]="${HERE}/specialists/endpoints/SKILL.md"
SKILLS[it-team-service-desk]="${HERE}/specialists/service-desk/SKILL.md"
SKILLS[it-team-identity-access]="${HERE}/specialists/identity-access/SKILL.md"
SKILLS[it-team-observability]="${HERE}/specialists/observability/SKILL.md"
SKILLS[it-team-ai-automation]="${HERE}/specialists/ai-automation/SKILL.md"
SKILLS[it-team-devops-platform]="${HERE}/specialists/devops-platform/SKILL.md"
SKILLS[it-team-interview-guide]="${HERE}/assessment/interview-guide.md"

VERSION="$(cat "${HERE}/VERSION" 2>/dev/null || echo unknown)"
echo "=== IT Team Framework v${VERSION} — Skill Sync (${MODE}) ==="
echo "Source: ${HERE}"
echo "Dest:   ${DEST}"
echo ""

SYNCED=0; SAME=0; DIFF=0; FAIL=0

for NAME in $(echo "${!SKILLS[@]}" | tr ' ' '\n' | sort); do
    SRC="${SKILLS[$NAME]}"
    [ -f "$SRC" ] || { echo "SKIP ${NAME}: missing ${SRC}"; continue; }
    TGT="${DEST}/${NAME}/SKILL.md"

    case "$MODE" in
      --check)
        if [ ! -f "$TGT" ]; then echo "MISSING  ${NAME}"; DIFF=$((DIFF+1))
        elif ! cmp -s "$SRC" "$TGT"; then echo "STALE    ${NAME}"; DIFF=$((DIFF+1))
        else echo "OK       ${NAME}"; SAME=$((SAME+1)); fi
        ;;
      --cli)
        if hermes skill create --name "${NAME}" --content "${SRC}" 2>/dev/null \
           || hermes skill update --name "${NAME}" --content "${SRC}" 2>/dev/null; then
            echo "CLI OK   ${NAME}"; SYNCED=$((SYNCED+1))
        else
            echo "CLI FAIL ${NAME} — run manually: hermes skill create --name ${NAME} --content \"${SRC}\""
            FAIL=$((FAIL+1))
        fi
        ;;
      *)
        mkdir -p "${DEST}/${NAME}"
        if [ -f "$TGT" ] && cmp -s "$SRC" "$TGT"; then
            SAME=$((SAME+1))
        else
            cp "$SRC" "$TGT" && { echo "SYNCED   ${NAME}"; SYNCED=$((SYNCED+1)); } \
                             || { echo "FAIL     ${NAME}"; FAIL=$((FAIL+1)); }
        fi
        ;;
    esac
done

# Legacy cleanup: it-team-security-gate was renamed to it-team-gatekeeper.
LEGACY="${DEST}/it-team-security-gate"
if [ -d "$LEGACY" ] && [ "$MODE" != "--check" ]; then
    if mv "$LEGACY" "${DISABLED}/legacy-it-team-security-gate-$(date +%Y%m%d)" 2>/dev/null; then
        echo "LEGACY   it-team-security-gate moved to disabled-skills/"
    else
        echo "LEGACY   it-team-security-gate present — remove manually (its SKILL.md should be a deprecation stub)"
    fi
fi

[ "$MODE" != "--check" ] && printf 'version=%s\ndate=%s\n' "$VERSION" "$(date -Iseconds)" > "${DEST}/.last-sync" 2>/dev/null || true

echo ""
echo "=== Summary: synced=${SYNCED} unchanged=${SAME} differing=${DIFF} failed=${FAIL} ==="
[ "$MODE" == "--check" ] && [ "$DIFF" -gt 0 ] && exit 1 || true
