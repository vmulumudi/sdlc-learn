# LEARNING Bravo

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
