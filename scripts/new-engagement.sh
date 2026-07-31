#!/bin/bash
# new-engagement.sh — Avvia un nuovo engagement IT Team Framework
# Uso: ./scripts/new-engagement.sh "Nome Azienda" [--size N] [--sector manufacturing] [--stack "..."] [--stdout]
#
# Crea una sessione Hermes preconfigurata con lo skill orchestrator
# e il contesto iniziale precompilato.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
    echo "Uso: $0 \"Nome Azienda\" [opzioni]"
    echo ""
    echo "Opzioni:"
    echo "  --size N           Numero dipendenti (default: chiesto durante intake)"
    echo "  --sector SETTORE   Settore merceologico"
    echo "    (manufacturing|logistics|finance|healthcare|services|retail|pa|other)"
    echo "  --stack \"...\"      Stack IT attuale (testo libero)"
    echo "  --stdout           Stampa il prompt invece di avviare hermes chat"
    echo "  -h, --help         Questo aiuto"
    echo ""
    echo "Esempi:"
    echo "  $0 \"TechSrl\" --size 50 --sector manufacturing"
    echo "  $0 \"LogisticaSpA\" --size 200 --sector logistics --stack \"VMware vSphere, AD, O365, SAP\""
    echo ""
    exit 0
}

# Valori di default
COMPANY=""
SIZE=""
SECTOR=""
STACK=""
STDOUT=false

# Parsing argomenti
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help) usage ;;
        --size) SIZE="$2"; shift 2 ;;
        --sector) SECTOR="$2"; shift 2 ;;
        --stack) STACK="$2"; shift 2 ;;
        --stdout) STDOUT=true; shift ;;
        -*|--*) echo "Opzione sconosciuta: $1"; usage ;;
        *) COMPANY="$1"; shift ;;
    esac
done

if [ -z "$COMPANY" ]; then
    echo "Errore: specifica il nome azienda"
    usage
fi

# Mappa settore → traduzione italiana
case "$SECTOR" in
    manufacturing) SECTOR_IT="Manifatturiero/Produzione" ;;
    logistics) SECTOR_IT="Logistica/Trasporti" ;;
    finance) SECTOR_IT="Finanza/Bancario/Assicurazioni" ;;
    healthcare) SECTOR_IT="Sanità" ;;
    services) SECTOR_IT="Servizi/Consulenza" ;;
    retail) SECTOR_IT="Retail/Commercio" ;;
    pa) SECTOR_IT="Pubblica Amministrazione" ;;
    other|"") SECTOR_IT="[specificare settore]" ;;
    *) SECTOR_IT="$SECTOR" ;;
esac

# Costruisci il prompt iniziale
PROMPT="Nuovo engagement IT Team Framework.

Carica skill: it-team-orchestrator

FASE 0 — INTAKE AZIENDALE

Nome azienda: ${COMPANY}
Settore: ${SECTOR_IT}"

if [ -n "$SIZE" ]; then
    PROMPT="${PROMPT}
Dipendenti: ${SIZE}"
fi

if [ -n "$STACK" ]; then
    PROMPT="${PROMPT}
Stack IT attuale: ${STACK}"
fi

PROMPT="${PROMPT}

Procedi con la Fase 0 (Intake) raccogliendo eventuali dati mancanti, poi Fase 1 (Assessment parallelo) con tutti i 9 specialisti, Fase 2 (Gate Review con it-team-gatekeeper), Fase 3 (Gap Analysis), Fase 4 (Roadmap) e presentami il risultato. Non eseguire automaticamente — presentami prima la roadmap per approvazione."

if [ "$STDOUT" = true ]; then
    echo "=== Prompt per Hermes ==="
    echo ""
    echo "$PROMPT"
else
    # Avvia hermes chat con il prompt
    echo "🚀 Avvio engagement per ${COMPANY}..."
    echo ""
    echo "hermes chat --eval \"\$PROMPT\""
    hermes chat --eval "$PROMPT"
fi