# Working on this skills library

## Scope

This repository owns these five skills: `h3-prompt-writing`, `kling-4-prompting`, `minimax-music-30`, `seedance-25`, and `suno-song-builder`. Preserve their complete reference, script, template, and agent-metadata folders. Do not publish unrelated installed skills or private creative assets.

## Local edits and GitHub updates

The owner's requested workflow is to update this repository whenever we update these skills locally. A Git-backed Hermes installation uses this checkout directly, rather than a second copied installation.

1. Confirm the checkout and origin are for `glitterpixely/skills`. Inspect the current branch, working-tree diff, and staged changes before editing. Read `CONTRIBUTING.md`.
2. Fetch origin. If the working tree is clean and the checked-out branch tracks the intended remote branch, use `git pull --ff-only`. Preserve existing work; never reset, overwrite, auto-stash, or force-push to resolve divergence. If concurrent edits or conflicts make intent unclear, ask the owner.
3. Edit the relevant skill files in the checkout. If an edit was made in a separate installed copy, compare it with the checkout and transfer only the intended changes; do not blindly mirror the whole skills directory.
4. Review the diff and run the relevant checks below. Preserve exact provider grammar and source attributions. Never commit credentials, private user materials, generated outputs, or machine-specific backups.
5. Stage only the reviewed task files, inspect `git diff --cached` and `git diff --cached --check`, then create a descriptive commit. For owner-authorized maintenance, push the intended branch to origin; respect branch protections and any request to use a pull request. Do not publish unrelated staged work.
6. Read back the remote branch with `git ls-remote origin refs/heads/<branch>` and compare its SHA with the pushed local commit. Only report synchronization after they match. On a push/authentication failure, retain local work and report that GitHub is not yet updated.

This is a task-completion workflow, not an unattended auto-push watcher. Local filesystem saves are visible to Git immediately; GitHub changes only after a successful commit and push.

## Validation

Run from this repository root:

```bash
python3 h3-prompt-writing/scripts/validate_coverage.py
python3 h3-prompt-writing/scripts/lint_h3_prompt.py --self-test
python3 seedance-25/scripts/validate_coverage.py
python3 seedance-25/scripts/prompt_lint.py --self-test
python3 minimax-music-30/scripts/validate_coverage.py
python3 minimax-music-30/scripts/lint_music_prompt.py --self-test
```

For Kling and Suno, check frontmatter and local reference links, and review the changed guidance. For shared documentation, verify links and instructions. Passing these checks is not proof of generated video or music quality.
