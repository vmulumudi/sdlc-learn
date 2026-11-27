# REVIEW CHECKLIST

Use when reviewing a teammate's work. Sections grow with each phase.

## Pull request
- [ ] Title follows Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `ci:`, `refactor:`, `test:`).
- [ ] PR is small and does one thing; unrelated changes split out.
- [ ] Template filled in: what/why, how tested, risk & rollback.
- [ ] All required checks green — and you know *which* checks are required (ruleset), not just "it's green".
- [ ] Branch is up to date with `main` (or the ruleset enforces it via strict status checks).
- [ ] No secrets, tokens, connection strings or `.env` files in the diff.
- [ ] Changes under `.github/workflows/`, `infra/`, or `CODEOWNERS` get extra scrutiny (they change *how* code ships).

## Repository settings / rulesets
- [ ] Default branch has a ruleset: block deletion and force-push, require PR, require status checks.
- [ ] Bypass list is empty (or a break-glass group, audited) — admins should not silently bypass.
- [ ] Merge strategy is deliberate (squash for linear, readable history) and branches auto-delete.
- [ ] CODEOWNERS covers `.github/workflows/` and `infra/`.

## Dockerfile
_(Phase 2)_

## Workflow (GitHub Actions)
_(Phase 6)_

## Bicep
_(Phase 7)_

## Container App config
_(Phase 7–8)_
