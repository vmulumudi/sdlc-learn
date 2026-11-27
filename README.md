# sdlc-learn

A practice version of a multi-component containerized product, used to learn the full
lifecycle: GitHub flow → local dev with Docker Compose → CI on GitHub Actions →
CD to Azure Container Apps via OIDC → promotion Dev → QA → Prod.

| Component | Tech | Folder |
|---|---|---|
| Frontend | React + Vite + TypeScript, served by nginx | `services/frontend` |
| API | Python FastAPI, PostgreSQL 16 + pgvector, Redis | `services/api` |
| Worker | Python, Azure Service Bus consumer, KEDA scale-to-zero | `services/worker` |
| Infra | Bicep (Container Apps, ACR, Postgres Flexible, Service Bus, Key Vault) | `infra` |

Azure: subscription *Pay-As-You-Go*, region **centralindia**, every resource tagged `project=sdlc-learn`.

## How we work
- `main` is protected by a repository **ruleset** (`.github/rulesets/main.json`): no direct pushes,
  PR required, required status checks, linear history.
- Branch → small commits → PR (template) → checks green → **squash merge** → branch auto-deleted.
- No secrets in the repo, ever. Azure auth from GitHub uses OIDC (Phase 8).

## Learning artifacts
- [LEARNING.md](LEARNING.md) — concepts, commands, gotchas per phase
- [BREAK-FIX-LOG.md](BREAK-FIX-LOG.md) — every injected failure: symptom, root cause, how found, guard
- [REVIEW-CHECKLIST.md](REVIEW-CHECKLIST.md) — what to check when reviewing a teammate's work
