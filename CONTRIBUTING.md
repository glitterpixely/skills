# Contributing

Useful contributions make a skill easier to follow, more accurate, or more effective for a concrete creative task.

## Report an issue

Include:

- The skill and file involved.
- The model version and platform or runtime, when relevant.
- What you expected and what actually happened.
- A minimal example, validator output, or a link to the relevant official documentation.

Remove credentials and private reference material from examples before posting.

## Propose a change

1. Keep each change focused on one skill or one shared documentation improvement.
2. Preserve the `SKILL.md` entry point, folder structure, and relative reference links.
3. Put detailed examples and supporting material in `references/`; keep the main workflow easy to navigate.
4. Support changed capability claims with primary sources, including the model version and the date checked. Distinguish observed behavior from documented support.
5. Run the relevant existing validation scripts and summarize the results in your pull request. For documentation-only changes, check links and examples.

Where available, run the skill’s coverage validator from the repository root:

```bash
python3 seedance-25/scripts/validate_coverage.py
python3 h3-prompt-writing/scripts/validate_coverage.py
python3 minimax-music-30/scripts/validate_coverage.py
```

Describe what changed, why it helps, and how it was checked. Keep prompt lint results separate from rendered-video inspection or listening tests; each establishes a different kind of evidence.

Preserve existing source attributions and identify the source and reuse terms of any third-party material you add.
