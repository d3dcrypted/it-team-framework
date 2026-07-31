# Changelog

Tutte le modifiche rilevanti del progetto sono registrate in questo file.

## [0.2.0] - 2026-07-31

### Added

- Versione del progetto in `VERSION`.
- Contratto comune di output per assessment e raccomandazioni.
- Severity canoniche: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
- Frontmatter Hermes uniformato per gli skill.
- Repository Git inizializzato per consentire diff, branch e tag.

### Changed

- Standardizzato il riferimento ai domini Identity & Access e Data, Backup & DR.
- Aggiunta la regola di re-gate quando un’azione cambia durante l’execution.

### Not yet implemented

- API ancora in modalità demo con raccomandazioni simulate.
- Test runtime FastAPI non ancora inclusi in questa release.
- Integrazione reale con Hermes ancora da implementare.

[0.2.0]: https://semver.org/
