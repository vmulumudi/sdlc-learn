# BREAK-FIX LOG

One entry per injected failure. Fill in after you diagnose it yourself.

| # | Phase | Break | Symptom (exact error) | Root cause | How I found it (commands/logs) | Fix | Guard added |
|---|---|---|---|---|---|---|---|
| 1 | 1 | Conflicting PRs |error when verifying pr hygine | the pr title is not according to the rules  | i checked it git hub view and found that the pr title is incorrect |changed the title to follow the rules | |
| 1b | 1 | Direct push to `main` | merge to main is giving error| earlier pr is merged which has changes in the same line - caused the error| i checked the error statement | fixed merge conflicts and then commit worked | |

EOF
