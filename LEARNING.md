# LEARNING Alpha

## Phase 1 — GitHub workflow

### Concepts (Azure DevOps → GitHub)
| Azure DevOps | GitHub | Notes |
|---|---|---|
| Azure Repos | Repository | Same git underneath. |
| Branch policies | **Rulesets** (or classic branch protection) | Rulesets are newer: can target many branches, can be exported as JSON, have an explicit bypass list. |
| Build validation policy | **Required status checks** | A check name produced by a workflow job must pass before merge. |
| Automatically included reviewers (by path) | **CODEOWNERS** | Path → owner. Becomes *required* only if the ruleset says "require review from code owners". |
| PR completion: merge / squash / rebase / semi-linear | Merge commit / squash / rebase | Configured per repo; we allow squash only. |
| Pipelines YAML | Actions workflows in `.github/workflows/` | Phase 6. |

**Good looks like:** `main` always deployable; no direct pushes; short-lived branches; PR template
filled in; required checks green; ≥1 code-owner approval (team) ; squash merge → one commit per PR;
branches auto-deleted after merge.

**Solo-repo reality:** GitHub never lets you approve your own PR, so this repo uses *required approvals = 0*.
In a team repo it should be ≥1 with "require review from code owners".

### Commands
```powershell
git switch -c feat/my-change          # new branch from current
git push -u origin feat/my-change     # publish branch, set upstream
gh pr create --fill                   # PR from commits (template applies in the web UI / --body-file)
gh pr checks                          # status of required checks
gh pr view --json mergeable,mergeStateStatus
gh pr merge --squash --delete-branch
git fetch origin; git rebase origin/main
git push --force-with-lease           # safe force push after rebase
```

### Gotchas
- Windows CRLF: `.gitattributes` forces LF so shell scripts work inside Linux containers.
- `--force-with-lease` refuses to overwrite remote commits you have not seen; plain `--force` does not.
- To see what *actually* applies to a branch (all rulesets combined), use
  `gh api repos/<owner>/<repo>/rules/branches/main` — not just the rulesets list.
- The first push to a new repo bypasses PR rules only because the ruleset doesn't exist yet
  ("bootstrapping"). After that, every change goes through a PR.
- Commit author email is public in a public repo. Use the GitHub noreply address
  (`<id>+<login>@users.noreply.github.com`) via `git config user.email`.

### Repo facts
- Repo: https://github.com/vmulumudi/sdlc-learn (public)
- Ruleset: `main-protection` (definition in `.github/rulesets/main.json`)
- Merge strategy: squash only; branches auto-delete on merge

### Learned in BREAK/FIX
- `strict_required_status_checks_policy: true` = "branch must be up to date before merging".
  Without it, two PRs can each pass CI alone and break `main` together (semantic conflict).
  Text conflicts are caught by git regardless; `strict` catches the ones git can't see.
- Editing `.github/rulesets/main.json` changes nothing by itself. Apply it with
  `gh api --method PUT repos/<owner>/<repo>/rulesets/<id> --input .github/rulesets/main.json`.
- A single-commit PR's squash title defaults to the **commit** message, not the PR title.
  So a PR-title check can pass while the bad title still lands on `main`.
- `git pull` saying "no tracking information" = the branch was pushed without `-u`.
  Fix: `git branch --set-upstream-to=origin/<branch>`.
- Direct push to `main` is rejected server-side with `GH013` (ruleset violation).

## Phase 2 — Backend API

### Run it
```powershell
docker compose up --build -d --wait   # postgres+pgvector, redis, migrate (one-shot), api
start http://localhost:8000/docs      # Swagger UI
docker compose down                   # add -v to also wipe the DB volume
```

### Concepts (Azure → this repo)
| Azure / ADO | Here | Notes |
|---|---|---|
| App Service health check / ACA probes | `/healthz` (liveness), `/readyz` (readiness) | Liveness checks no deps; readiness fails only on hard deps (Postgres). |
| ACA Job / pipeline migration step | `migrate` service = same image, `alembic upgrade head` | Migrations run once before the new revision gets traffic. |
| Azure Cache for Redis (cache-aside) | `X-Cache: HIT/MISS` on `GET /api/notes/{id}` | Cache is optional: failures never fail requests. |
| Azure OpenAI embeddings | `app/embedding.py` hash-based stand-in | Zero cost; swap later, only `EMBEDDING_DIM` changes. |

### Gotchas
- A slow, dead cache is worse than no cache: 1s Redis timeouts made every read take 2s.
  Fixed with a 30s circuit breaker in `app/cache.py`.
- Windows PowerShell 5.1: `Invoke-WebRequest` needs `-UseBasicParsing` in scripts; or use `curl.exe`.
- pgvector on Azure Flexible Server requires allow-listing `VECTOR` in `azure.extensions` first.
