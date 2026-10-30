<div align="center">

# ✦ Contributing to Creative AI Skills Studio ✦

*Useful contributions make a skill easier to follow, more accurate, or more effective for a concrete creative task.*

<img src="assets/divider-pastel.svg" alt="" width="100%" />

</div>

## 1. Report an Issue

When opening an issue, please include:

- **Skill & file:** Which skill folder and reference/script file are involved.
- **Model & surface:** The model version (e.g., Seedance 2.5, MiniMax H3, Kling 4.0, Suno v6, MiniMax Music 3.0) and platform or runtime, when relevant.
- **Expected vs. actual:** What you expected the prompt or validator to do and what actually happened.
- **Reproducible evidence:** A minimal example brief, validator output, or a link to the relevant official documentation.

> **Privacy note:** Always remove API keys, credentials, and private reference material from examples before posting.

---

## 2. Propose a Change

1. **Stay focused:** Keep each pull request scoped to one skill or one shared documentation improvement.
2. **Preserve portability:** Keep the `SKILL.md` entry point, folder structure, and relative `references/` and `scripts/` links intact.
3. **Keep `SKILL.md` lean:** Place detailed examples, academic tables, and supporting material in `references/` so the main workflow stays fast to scan.
4. **Cite primary sources:** Support changed capability claims with official documentation or peer-reviewed research, including the model version and the date checked. Distinguish observed behavior from documented guarantees.
5. **Run the validators:** Run the relevant validation scripts from the repository root and include the results in your pull request description:

```bash
python3 seedance-25/scripts/validate_coverage.py
python3 h3-prompt-writing/scripts/validate_coverage.py
python3 minimax-music-30/scripts/validate_coverage.py
```

Keep prompt lint results separate from rendered-video inspection or listening tests—each establishes a different kind of evidence. Preserve existing source attributions and identify the source and reuse terms of any third-party material you add.

<div align="center">
  <br />
  <img src="assets/footer-stamp.svg" alt="crafted with care · glitterpixely studio" width="260" />
</div>
