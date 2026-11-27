# LEARNING

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
