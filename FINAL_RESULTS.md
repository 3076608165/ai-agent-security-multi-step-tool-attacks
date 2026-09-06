# FINAL RESULTS

Authoritative record of the final submission and result. Every figure below was
read back from the Kaggle CLI / leaderboard on this machine, not recalled.

## Result

- **Competition**: [AI Agent Security: Multi-Step Tool Attacks](https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks)
- **Team**: `UTS_25522741` (teamId `16746252`, account `uts3125025522741`)
- **Final private score**: **26.52000**
- **Final rank**: **#42 / 4186** → **Silver Medal** (awarded September 2026)
- Public best: **87.975** (#989 / 4187) via the `http.post` exfil engine (which scores 0 on private)

## Final submission

Finals were private-only and selected as **DEPUTY + DEPUTY** (two slots, both the
`email.send` confused-deputy engine — the only private scorer; exfil self-cancels
on the private guardrail).

| Slot | Submission | ref | pub | priv |
|------|-----------|-----|-----|------|
| Final #1 | deputy v3 — frontier single-note | 55834276 | 26.520 | 26.520 |
| Final #2 | deputy farm roll 2 | 55861384 | 26.355 | 26.355 |

The medal engine is **`attack_private.py`** (CONFUSED_DEPUTY `email.send`, single-note,
race-classify + fastest-first sort + `REPLAY_COST_COEF=0.95` + `REPLAY_SAFE_FRAC=0.985` +
"Then say OK."), byte-embedded in `submission_notebook.ipynb`.

Notebook script versions: exfil = `345124354`, deputy = `345522567` (`-v` on submit).

## Code hashes (SHA-256, exact files as of this commit)

| File | sha256 |
|------|--------|
| `attack_private.py` (medal engine) | `ad6fb6de2cefc2c64569cbdebf9536480f6efd7f2343b5b771c4f17b304d37b5` |
| `attack.py` (public exfil v8) | `b16c7630d147e2a7b394e0ee889dddea3face2853d839a085c6b1e5974f6b380` |
| `submission_notebook.ipynb` (embeds medal engine) | `3ba0db11a8e6fe2e83fc328061b2a33c162223b35a365da0b4f2b8f43a595d64` |

## Links

- Notebook: https://www.kaggle.com/code/uts3125025522741/notebook3497b27639
- Leaderboard: https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/leaderboard
- Submissions: https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/submissions

## Reproduce

1. Download the competition data so `official/aicomp_sdk` is present (git-ignored here).
2. `pip install -r requirements.txt` (pinned offline-validation deps).
3. `python -m pytest tests/ -v` — verifies both engines run offline AND that the
   notebook embeds `attack_private.py` byte-for-byte.
4. The medal is not reproducible locally (it needs the hosted GPT-OSS / Gemma sandbox);
   re-submit `submission_notebook.ipynb` on Kaggle to re-run the exact engine.

## Known limitations (honest)

- `attack.py` is the **v8 multipost-off** public variant, not the **v9** engine whose
  roll hit 87.975. The v9 exfil engine is the exfil analog of `attack_private.py`'s
  frontier structure (its submission is documented above, ref 55808181); a byte-clean
  v9 root file was not retained.
- `experiments/submission.csv` and per-snapshot `submission.csv` files are zero
  placeholders from the submission tooling, not scores.
