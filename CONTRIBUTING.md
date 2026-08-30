# Contributing Guide

This document defines how our 4-person team works in this repository:
branching strategy, commit conventions, versioning, and the PR process.
Following this consistently is what makes the repo defensible as "industry
practice" in a supervisor review or viva.

## 1. Branching Strategy — Trunk-Based with Short-Lived Feature Branches

We use a simplified **trunk-based development** model, appropriate for a
small team and a project of this size (full GitFlow with `develop`/`release`
branches is overkill for a 4-person FYP and adds process cost with no
real benefit at this scale).

```
main                    ← always deployable, protected branch
 ├── feature/h1-voice-emotion-model
 ├── feature/h2-memory-store
 ├── feature/h3-baseline-condition
 ├── fix/asr-timeout-handling
 └── docs/ethics-consent-update
```

### Branch naming convention

| Prefix | Use for |
|---|---|
| `feature/` | New functionality (e.g. `feature/wav2vec2-inference`) |
| `fix/` | Bug fixes (e.g. `fix/chroma-connection-retry`) |
| `docs/` | Documentation-only changes |
| `refactor/` | Code restructuring with no behavior change |
| `test/` | Adding or fixing tests |
| `chore/` | Tooling, CI, dependency bumps |

### Rules

- **Never commit directly to `main`.** Always branch, commit, open a PR.
- Keep branches short-lived (days, not weeks) — merge often to avoid painful conflicts.
- One branch = one logical unit of work (e.g. don't mix H1 model work and H2 memory work in the same branch).
- Delete branches after merging.

## 2. Commit Message Convention — Conventional Commits

We use [Conventional Commits](https://www.conventionalcommits.org/) so the
history is machine-readable (enables auto-generated changelogs) and
human-readable (easy to scan `git log` during thesis writing).

```
<type>(<scope>): <short summary>

[optional body]

[optional footer]
```

### Types
| Type | Use for |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `test` | Adding/fixing tests |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `chore` | Tooling, CI, dependencies |
| `perf` | Performance improvement |

### Examples
```
feat(emotion): add Wav2Vec2 comparison classifier for H1

fix(memory): scope Chroma queries by participant_id to prevent data leakage

docs(ethics): add data retention policy to consent template

test(memory): add participant isolation test for H2 memory store
```

### Scopes used in this repo
`asr`, `tts`, `emotion`, `memory`, `llm`, `conditions`, `ui`, `config`, `docs`, `ci`, `tests`

## 3. Versioning — Semantic Versioning

We tag releases using [SemVer](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR** — breaking changes to the study protocol or data schema (should be rare/avoided mid-study)
- **MINOR** — new features (e.g. adding Session 3, adding the admin dashboard)
- **PATCH** — bug fixes, small tweaks

See `CHANGELOG.md` for the human-readable history of what changed at each version.

### Suggested milestones for this project
| Version | Milestone |
|---|---|
| `v0.1.0` | Initial scaffold (this commit) |
| `v0.2.0` | H1 models trained and evaluated |
| `v0.3.0` | H2 memory pipeline functional end-to-end |
| `v0.4.0` | H3 baseline + integrated conditions complete |
| `v0.5.0` | Deployed to Streamlit Cloud, pilot-tested |
| `v1.0.0` | Ethics-approved, ready for the real 20-participant study |

To tag a release:
```bash
git tag -a v0.2.0 -m "H1 models trained and evaluated"
git push origin v0.2.0
```

## 4. Pull Request Process

1. Branch off `main`.
2. Make your changes, following the commit convention above.
3. Run tests locally before opening a PR: `pytest`
4. Run the formatter/linter: `pre-commit run --all-files` (see Section 5)
5. Open a PR into `main` using the PR template (auto-populated).
6. **At least one other team member must review and approve** before merging — this is the single most important practice for a 4-person team, since it catches bugs and keeps everyone aware of the whole codebase (important when 3 of you may need to speak to any part of it in a viva).
7. Squash-merge or merge normally (either is fine for a project this size — just be consistent).
8. Delete the branch after merging.

## 5. Code Style & Pre-commit Hooks

We use `black` (formatting), `ruff` (linting), and `isort` (import ordering),
enforced automatically via pre-commit hooks.

### One-time setup (each team member)
```bash
pip install pre-commit
pre-commit install
```

After this, every `git commit` automatically runs formatting/lint checks.
See `.pre-commit-config.yaml` for the exact hook configuration.

## 6. Continuous Integration

Every push and PR automatically runs the test suite and linter via GitHub
Actions (see `.github/workflows/ci.yml`). A PR cannot be merged if CI fails
— configure this as a required check in the repo's branch protection
settings (Settings → Branches → Add rule → require status checks to pass).

## 7. Issue Tracking

Use GitHub Issues to track work, using the templates in
`.github/ISSUE_TEMPLATE/`. Suggested labels: `h1`, `h2`, `h3`, `bug`,
`documentation`, `ethics`, `good-first-issue`.

## 8. Protecting `main`

On GitHub: **Settings → Branches → Add branch protection rule** for `main`:
- Require a pull request before merging
- Require at least 1 approval
- Require status checks (CI) to pass before merging
- Do not allow force pushes

This is free on GitHub for private repos with a small team and takes two minutes to set up — do this before your team starts writing real study code.
