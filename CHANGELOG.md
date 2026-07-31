# Changelog

## [Unreleased]

### Added

- MIT license, portable systemd service template, CI workflow and tracked-file secret scan for public distribution.
- Contributor workflow defining branch naming, pull requests, validation, and release rules.

### Changed

- Updated API security guidance for production mode and marked model records as demonstration seeds.

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
