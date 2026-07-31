# Contributing

## Branch policy

`main` is the protected, releasable branch. Do not push directly to `main`.

Create a short-lived branch from the latest `main`:

```bash
git switch main
git pull --ff-only origin main
git switch -c <type>/<short-description>
```

Use one of these branch prefixes:

- `feature/` — new functionality
- `fix/` — bug fix
- `docs/` — documentation-only change
- `test/` — tests and validation
- `chore/` — maintenance, CI, or repository administration

## Pull requests

Every change must be submitted as a pull request targeting `main`.

Before opening a pull request:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/pytest -q
```

The CI workflow must pass. A pull request should contain:

- a concise description of the change;
- the validation performed;
- documentation or changelog updates when behavior or public structure changes;
- no secrets, credentials, personal data, databases, reports, or local environment files.

Keep pull requests focused. Avoid mixing unrelated refactors with functional changes.

## Commit messages

Use an imperative, scoped message where practical:

```text
<type>: <short description>
```

Examples: `docs: clarify deployment model`, `fix: reject invalid gate transition`.

## Releases

Releases are created from a reviewed and merged commit on `main`. Update `VERSION` and `CHANGELOG.md`, run the complete test suite, then create an annotated semantic-version tag.

## Security

Do not report vulnerabilities in public issues. Follow the repository's security reporting process when one is configured. Never commit tokens, passwords, API keys, private keys, or customer data.
