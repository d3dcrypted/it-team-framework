# Changelog

## [0.4.1] - 2026-11-26

### Fixed

Second pass on 0.4.0, probing the API instead of re-reading it. Each item was reproduced first.

- **Gate decisions are frozen once the gate closes.** A decision could still be changed in `roadmap_ready`, so the roadmap that reached execution was not necessarily the one the gate passed. Decisions are accepted only in `gate_review`.
- **An engagement cannot complete with unfinished actions.** `POST /engagements/{id}/complete` checked the verdict only; it returned 200 with one action `RUNNING` and one `PENDING`.
- **Actions run only while the engagement is `executing`.** `actions/{id}/start` did not look at the engagement state.
- **A blank `evidence_ref` is no evidence.** A single space satisfied the `VALIDATED` precondition.
- **Two endpoints still leaked the connection on error.** `GET /recommendations` and `GET /roadmap` kept the `get_conn()`/`close()` pair that 0.4.0 said it had replaced everywhere.
- **The systemd unit no longer claims to work as-is.** It ran in `production` with the environment file commented out, so it refused to start. The file is now referenced, and the comment says what `production` does without an adapter: it authenticates, and assessment fails.

### Documented

- The API enforces workflow order, not identity. One shared key; `reviewed_by`, `validator_agent` and `executor_agent` are caller-supplied. Stated in the README and the module docstring.

## [0.4.0] - 2026-11-26

### Fixed

Everything below comes from an external review of the public repository (`api/server.py` was read line by line, and the behaviour below was reproduced against a running server).

- **The gatekeeper review now blocks.** `POST /engagements/{id}/gate-review` called `set_status("gate_review")` and `set_status("roadmap_ready")` in the same request, so the review was never a state anything could fail. The gate is now opened and closed by two separate calls; the new `POST /engagements/{id}/gate-review/close` passes only when every recommendation has a decision and at least one is approved, and records the transition as `it-team-gatekeeper`.
- **An all-rejected roadmap can no longer be executed.** `POST /engagements/{id}/execute` required only that no recommendation be undecided; three `DENIED` decisions satisfied that. It now also requires at least one approval.
- **Self-validation can no longer be bypassed.** `executor_agent` was optional on `POST /engagements/{id}/validator-verdict`, and the independence check `validator_agent != executor_agent` was the only rule that consumed it: omitting the field skipped it. The field is required, and `engagement_id` in the body is rejected with 409 when it contradicts the path.
- **A verdict can no longer precede execution.** Verdicts are accepted only while the engagement is `executing`, and a `VALIDATED` verdict must carry `evidence_ref`: a verdict without evidence is the assumption the validation gate exists to stop.
- **Dependency rules are enforced, not described.** The graph was stored and never checked. It is now validated on write (unknown predecessors, self-dependencies and cycles are rejected with 422) and enforced at execution time: `POST /engagements/{id}/actions/{action_id}/start` answers 409 while any predecessor is not `COMPLETED`, `POST .../complete` requires the action to be `RUNNING`, and `GET /engagements/{id}/actions` reports each action's state and what blocks it.
- **Concurrent state changes no longer overwrite each other.** `set_status` read the current state and then wrote unconditionally. It now compares and swaps (`UPDATE ... WHERE id = ? AND status = ?`), accepts the transition only if the row matched, and reuses the `TRANSITIONS` table instead of a separate validity set. Two racing requests cannot both succeed from the same state.
- **Database connections are always closed.** Every `get_conn()`/`close()` pair left the connection open on the error paths that returned early or raised. A single `db()` context manager commits on success and closes in a `finally`, and replaces all of them, including `init_db()`.
- **Demo mode is no longer silently unauthenticated.** Authentication was applied only when `MODE == "production"`, so a configured `IT_TEAM_API_KEY` was ignored in demo. A key that is set is now enforced in every mode; demo without a key stays open, loopback only, as `docs/configuration.md` states.
- **The systemd unit is valid.** `User=%i` resolves only for template units; installed as a plain unit, systemd rejects the file with `Invalid user/group name or numeric ID`. The supplied file is now a user unit that verifies clean and runs as-is (`systemd-analyze --user verify` exits 0); `docs/deployment-architecture.md` keeps the system-wide example with a dedicated user.

### Changed

- `tests/test_api_v02.py` extended to cover the gate failure path, the verdict preconditions and the dependency enforcement: 4 tests → 7, still dependency-free and deterministic.

## [0.3.4] - 2026-11-26

### Changed

- **README rewritten in plain prose, authorship documented.** The dash-heavy opener and the "not just technical skills" line are gone, and a `## Authorship` section states the split plainly: the direction and the review are the author's, the drafting is an AI assistant's. Documentation only, no behaviour change.

## [0.3.3] - 2026-11-26

### Changed

- **All 17 skill descriptions compressed to ≤60 chars.** Frontmatter `description` was 113–242 chars, which bloated the skill index every session pays for. Each is now a `Use when <trigger>: <key content>.` line (113–242 → 48–60), same domains and tooling, no behaviour change. Edited in the repo (canonical), then `scripts/deploy-skills.sh` re-synced the installed copies.

## [0.3.2] - 2026-11-26

### Fixed

- **CI was red on the v0.3.1 commit.** `tests/test_api_v02.py` still asserted the pre-0.3.1 contract (auto-`completed` after `execute`, `version == "0.2.0"`). The lifecycle test now walks the validation gate end to end: `executing` after `execute`, 409 on `complete` without a verdict, 409 on self-validation, `completed` only after a `VALIDATED` verdict, and the audit trail records the transition.
- **Version drift removed.** `api/server.py` reads the repo-root `VERSION` file for both the FastAPI app version and `/health`, instead of two hand-edited copies plus the test's third copy.
- **Public tree carries no personal identity.** Skill frontmatter uses `author: Hermes Agent`, the LICENSE holder is the public handle, and `model-strategy.md` no longer ships an unrendered `$(date)`/personal line.

### Changed

- Model strategy updated: default `openai/gpt-5.6-luna` (€0.21/1k) + `mimo-v2.5-free` → `deepseek/deepseek-v4-flash` ($0.019-0.021/1k) + `typesafe/jev-router` ($0.042/M input, $0 output). `model-strategy.md` and `orchestrator/SKILL.md` updated with active config as of 2026-09-29.
- Active aliases: `local` = `qwen3` (Ollama). OmniRoute still down; revert to `auto/*` when back.

## [0.3.1] - 2026-08-18

### Added (P1 — the upgrade decided earlier; P0 shipped in 0.3.0)

- **Real validation, not aspirational** (P1): the orchestrator MUST dispatch `it-team-validator` as a separate agent/session after every `IMPLEMENTED` action. `COMPLETED` is set only after a `VALIDATED` verdict. Skipping the dispatch is now a defined framework defect.
- **API enforcement of the validation gate**: new endpoints `POST /engagements/{id}/validator-verdict` (records the independent verdict; rejects self-validation where `validator_agent == executor_agent` with 409) and `POST /engagements/{id}/complete` (rejects with 409 unless a `VALIDATED` verdict exists). The old `execute` path no longer auto-marks `completed`.
- **Dependency-checked execution** (P1): every roadmap action carries `depends_on: [action_ids]`; actions with unmet predecessors stay `BLOCKED`. `POST /engagements/{id}/dependencies` records the graph; the orchestrator computes a topological order and aborts on cycles.
- **Append-only audit trail** (P1): `state_transitions` table records every status change once (from_state, to_state, changed_at, changed_by) and is never updated or deleted. `GET /engagements/{id}/audit-trail` exposes it; the live `status` column is a cache of the latest row.

### Fixed (model leak + drift — found post-ship)

- **Model leak closed** (the incident pattern): `orchestrator/SKILL.md` `Recommended Model Configuration` no longer seeds `openai/gpt-5.6-luna` via `provider: openrouter` (the exact config that burned ~$55/day). Replaced with `auto/best-reasoning` / `auto/best-coding` aliases plus a binding cost-leak rule. Pitfall #6 updated: data routes through configured LLM routing (OmniRoute), not OpenRouter.
- **Skill naming drift (P2)**: `assessment/interview-guide.md` frontmatter `name` corrected `it-team-assessment-guide` -> `it-team-interview-guide`; `docs/deployment-architecture.md` tree updated to match. The dangling `assessment-guide` reference is gone.
- **Engagement state artifact (P1 resumability)**: new `## Engagement State Artifact` contract — one `engagement-state.md` persisted per engagement and resumed by `phase` if a session dies mid-flow.

### Changed

- `api/server.py`: version reported by `/health` bumped `0.2.0` -> `0.3.1`; `set_status` now writes the append-only audit row.

### Rationale

P0 (validator skill, evidence rules, post-execution states) was contract-only — an agent could still mark `COMPLETED` by assumption. P1 closes that gap: the validation is enforced by code, execution order is dependency-bound, and state history is tamper-evident.

## [0.3.0] - 2026-08-01

### Added

- Four new specialists for medium-to-large organization coverage: `identity-access` (fills the v0.2 contract gap — the domain existed with no specialist), `observability`, `ai-automation`, `devops-platform`.
- Independent Technical Validator (`validator/SKILL.md`): evidence-based post-execution verification. `COMPLETED` now requires a `VALIDATED` verdict from a non-executing agent (v0.3 P0).
- Execution states contract: `PLANNED → IN_PROGRESS → (BLOCKED) → IMPLEMENTED → VALIDATED → COMPLETED` (v0.3 P0).
- Evidence requirements with weights (command output / KPI delta / dated report; executor statements weigh zero) (v0.3 P0).
- Contract precedence rule: `orchestrator/SKILL.md` is the single source of truth for severities, SLAs, schemas, domain names, and states.
- Change awareness rule: orchestrator reads `VERSION` + `CHANGELOG.md` at engagement start and requests a skills re-sync when installed skill versions differ.
- `scripts/deploy-skills.sh`: one-way sync repo → `~/.hermes/skills/it-team/` making the repo the only canonical source (stale-copy drift eliminated).
- (from Unreleased) MIT license, portable systemd service template, CI workflow and tracked-file secret scan for public distribution.
- (from Unreleased) Contributor workflow defining branch naming, pull requests, validation, and release rules.

### Changed

- All 9 v0.2 specialists: local (divergent) Severity Levels tables replaced with a reference to the orchestrator contract; version aligned to 0.3.0.
- Gatekeeper: domain enum extended to 13; distinction from validator documented.
- Recommended model configuration updated (seeds: gpt-5.6-luna orchestrator / mimo-v2.5 workers; delegation `max_iterations` 50 → 30, `max_concurrent_children` capped at 3).
- (from Unreleased) Updated API security guidance for production mode and marked model records as demonstration seeds.

### Rationale

Recorded for orchestrator awareness: coverage extended to medium/large-company IT teams; validation added because v0.2 allowed unverified COMPLETED; dedup performed because two divergent copies of contract values (repo vs installed skills, 48h vs 24h CRITICAL SLA) risked contradictory agent behavior.


All significant project changes are recorded in this file.

## [0.2.0] - 2026-07-31

### Added

- Project version in `VERSION`.
- Common output contract for assessments and recommendations.
- Canonical severities: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
- Unified Hermes frontmatter for skills.
- Git repository initialized to enable diffs, branches, and tags.

### Changed

- Standardized references to the Identity & Access and Data, Backup & DR domains.
- Added the re-gate rule when an action changes during execution.

### API and validation

- Demo API made deterministic with a state machine, four-outcome gatekeeper decisions, idempotency, and consistent error handling.
- Added automated API lifecycle tests and the Acme Logistics example use case.
- Real Hermes integration still to be implemented; demo mode remains explicit.

[0.2.0]: https://semver.org/
