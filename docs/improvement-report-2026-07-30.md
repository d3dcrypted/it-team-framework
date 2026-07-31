# Report Migliorie — IT Team Framework

Data: 2026-07-30. Analisi completa partendo dal README.md, con migliorie applicate per categoria.

## 1. Gap strutturale critico: Gatekeeper mancante (RISOLTO)

Il README, la tabella ruoli, il flusso di lavoro e l'API referenziavano tutti un Security Gatekeeper con `gatekeeper/SKILL.md`, ma **il file non esisteva** e l'orchestrator non aveva alcuna fase di Gate Review. Interventi:

- Creato `gatekeeper/SKILL.md` (`it-team-gatekeeper`): criteri di review (sicurezza, compliance, continuità, privilegi, dati, dipendenze), 4 esiti (APPROVED / APPROVED_WITH_CONDITIONS / CHANGES_REQUESTED / DENIED), formato input/output, regole operative e pitfall. Coerente con gli endpoint gate-review dell'API.
- `orchestrator/SKILL.md`: inserita la Fase 2 Gate Review (diagramma + workflow); rinumerate le fasi (Gap Analysis→3, Roadmap→4, Execution→5); aggiornati esempio d'uso e verification checklist; aggiunto `it-team-gatekeeper` alle related_skills.
- `scripts/deploy-skills.sh`: aggiunto il deploy dello skill gatekeeper (prima non veniva mai installato).
- `scripts/new-engagement.sh`: il prompt generato ora include la Gate Review nel flusso.

## 2. README — incoerenze corrette

- Tabella ruoli: il Security Gatekeeper era conflato con lo specialista Security; ora sono due righe distinte (CISO/Gatekeeper = gate trasversale; Security Engineer = assessment del dominio). Descrizione orchestrator corretta da "10 specialist agents" a "9 specialisti + gatekeeper".
- Sezione Privacy: la frase "nessun dato lascia il tuo ambiente" contraddiceva l'uso di OpenRouter (ammesso nei pitfall dell'orchestrator). Riscritta in modo onesto: i prompt transitano via OpenRouter; mitigazioni elencate; rimando ai modelli locali per privacy totale.
- Prezzo ling-2.6-flash: README diceva $0.04/M, il doc modelli $0.10/$0.30 per 1M. Allineato al doc.
- Aggiunta sezione "API di Gestione" (prima l'API non era documentata da nessuna parte): avvio, endpoint principali, avvertenza sull'autenticazione.

## 3. API (`api/server.py`) — sicurezza e modernizzazione

- **CORS insicuro**: `allow_origins=["*"]` + `allow_credentials=True` è una combinazione non valida/pericolosa → credentials disabilitate.
- **Nessuna autenticazione**: aggiunta auth opzionale Bearer via env `IT_TEAM_API_KEY` (se non impostata, comportamento invariato; `/health` sempre libero).
- **API deprecate**: `@app.on_event("startup")` → lifespan; `datetime.utcnow()` → `datetime.now(timezone.utc)`.
- **Path hardcoded**: `DB_PATH` ora da env `IT_TEAM_DB_PATH` con default relativo al file.
- **Bug funzionale**: `EngagementCreate.description` veniva accettato ma mai salvato → ora persistito e restituito.
- **Dati incoerenti**: la tabella models conteneva modelli estranei al framework (gpt-4o, claude-3-opus, mixtral) con costi per 1k token → sostituiti con deepseek-v4-flash e ling-2.6-flash, costi input/output per 1M allineati a `docs/model-budget-analysis.md`.
- `it-team-api.service`: bind cambiato da `0.0.0.0` a `127.0.0.1` (esposizione pubblica solo dietro reverse proxy), aggiunte env commentate per API key e DB path.

## 4. Script

- `deploy-skills.sh`: rimossa variabile `CONTENT` morta (leggeva l'intero file senza usarlo); aggiunto gatekeeper.
- `new-engagement.sh`: l'help citava un'opzione `--emoji` inesistente → sostituita con le opzioni reali `--stack`/`--stdout`; prompt aggiornato con le fasi corrette.

## 5. Skill specialisti — standardizzazione e correzioni

- **Frontmatter rotti**: `applications` (metadati fuori dal blocco YAML) e `network` (nessun frontmatter) ora hanno YAML valido con name/description/category/version/author/license.
- **Frontmatter standardizzati**: aggiunti version/author/license mancanti (os-infra, data, endpoints, budget, service-desk); categorie corrette (budget e service-desk erano "devops", endpoints era "it-team"); aggiunta category a cloud e security. Tutti i 12 file ora hanno YAML valido (verificato con parser).
- **security**: rimosso testo in polacco ("MFA on wszystkich accounts"), corretto errore comune #1 sgrammaticato, "DPO" → "DPIA" per il Data Protection Impact Assessment, corretta ripetizione GoPhish/Gophish.
- **network**: "iperIperf"→iperf, "Redondanza"→Ridondanza, "Installa/Nest"→Installa, "top TALKER"→top talker.
- **service-desk**: "Completzza"→Completezza, "Taglife cycle"→Lifecycle, "certificationi"→certificazioni, "Moduli modulo"→Moduli di compilazione.
- **endpoints**: "PXE/UFE"→PXE/UEFI.
- **budget**: "Vendor Consolidification"→Vendor Consolidation; rimosso footer placeholder "Last updated: Current session".

## 6. Docs

- `model-budget-analysis.md`: corretta riga di tabella rotta (un `\n` letterale univa Claude Sonnet e Mixtral nella sezione Professional); rimosso inciso errato "(≈ €1,200 / mese)" nella fascia Budget 20-40 €.

## Verifiche eseguite

- `bash -n` su entrambi gli script: OK.
- `python3 -m py_compile api/server.py`: OK.
- Parse YAML dei frontmatter di tutti i 12 file skill: OK.
- Grep incrociato: gatekeeper referenziato coerentemente in README, orchestrator, deploy script e new-engagement; nessun residuo di "$0.04/M" o `\n` letterali.
- **Non verificato**: test runtime dell'API (fastapi non installabile nella sandbox senza rete) e comandi `hermes` CLI (non disponibili qui). Consigliato uno smoke test locale: `uvicorn server:app` + `curl /health`.

## Raccomandazioni residue (non applicate)

1. **Lingua mista**: i file alternano italiano e inglese anche all'interno dello stesso documento (os-infra, data, endpoints, budget in inglese; gli altri in italiano). Uniformare richiederebbe una riscrittura estesa — da decidere la lingua target.
2. **Modello del gatekeeper**: valutare un modello più capace di ling-2.6-flash per la gate review (è il punto di controllo di sicurezza; un worker economico può approvare troppo facilmente).
3. **API demo**: `assess` ed `execute` generano dati fittizi; se l'API deve diventare operativa, andrà collegata a Hermes (delegate_task reali).
4. **Versioning**: aggiungere un CHANGELOG.md e taggare le versioni degli skill quando si modificano.
