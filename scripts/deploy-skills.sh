#!/bin/bash
# deploy-skills.sh — Installa tutti gli skill IT Team Framework in Hermes
# Uso: ./scripts/deploy-skills.sh
# Richiede: hermes CLI disponibile e configurato

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HERE="${SCRIPT_DIR}"

echo "=== IT Team Framework — Deploy Skills ==="
echo "Origine: ${HERE}"
echo ""

# Mappa: nome skill → percorso SKILL.md
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
        echo "⚠️  SKIP: ${NAME} — file non trovato: ${PATH_FILE}"
        continue
    fi

    echo -n "→ ${NAME} ... "

    # Prova a creare/aggiornare lo skill
    if hermes skill create --name "${NAME}" --content "${PATH_FILE}" 2>/dev/null; then
        echo "✅ creato"
    elif hermes skill view "${NAME}" >/dev/null 2>&1; then
        # Già esiste — lo aggiorniamo via skill_manage (da dentro Hermes)
        # Per CLI, proviamo a usare il comando skill update se esiste
        if hermes skill update --name "${NAME}" --content "${PATH_FILE}" 2>/dev/null; then
            echo "✅ aggiornato"
        else
            echo "⚠️  esiste (usa /skill ${NAME} per caricarlo)"
        fi
    else
        echo "❌ fallito — crealo manualmente con:"
        echo "   hermes skill create --name ${NAME} --content \"${PATH_FILE}\""
        FAIL=$((FAIL + 1))
    fi
    COUNT=$((COUNT + 1))
done

echo ""
echo "=== Riepilogo ==="
echo "Installati: ${COUNT}"
echo "Falliti: ${FAIL}"
echo ""
echo "Per usare: avvia hermes chat e carica lo skill orchestrator:"
echo "  /skill it-team-orchestrator"
echo "Poi spiega il contesto aziendale."