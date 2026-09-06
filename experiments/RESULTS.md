# Final results — unified table

Single source of truth for the competition outcome, distilled from the Kaggle
submission log (`kaggle competitions submissions`) and the leaderboards. Raw
per-snapshot artifacts live in this directory; this file is the summary.

## Medal & final leaderboard placement

| Board | Engine | Score | Rank |
|-------|--------|-------|------|
| Public | `http.post` exfil (v9 frontier) | **87.975** | #989 / 4187 |
| Private (final) | `email.send` confused deputy (deputy v3) | **26.520** | **#42 / 4186 — Silver** |

Finals (private-only) were selected as **DEPUTY + DEPUTY**:
`deputy v3` (26.520) + best `deputy farm` roll (26.355).

## Final selections

| Role | Submission | ref | Score (pub/priv) |
|------|-----------|-----|------------------|
| Final #1 | deputy v3 — frontier single-note | 55834276 | 26.520 / 26.520 |
| Final #2 | deputy farm roll 2 | 55861384 | 26.355 / 26.355 |

## Key milestone submissions

### `http.post` exfil engine (public board; private = 0 by guardrail)

| Date | Submission | pub | ref |
|------|-----------|-----|-----|
| 2026-08-26 | v9 frontier — Then say OK + race-classify + fastest-first + 0.985/0.95 | 87.075 | 55795422 |
| 2026-08-27 | **resubmit v9 roll 2 (peak)** | **87.975** | 55808181 |
| 2026-08-27 | resubmit v9 roll 5 | 84.825 | 55808190 |
| 2026-08-23 | v3 token-forge + split-latency + replay-safe | 86.250 | 55707208 |
| 2026-08-25 | v7 single-post recipe (N=1 + Then say OK) | 84.420 | 55759703 |
| 2026-08-26 | v8 — replay-packing (COST_COEF 0.95 / SAFE_FRAC 0.985) | 77.655 | 55795044 |
| 2026-08-29 | exfil farm roll 2 | 86.130 | 55861391 |

### `email.send` confused-deputy engine (scores on BOTH boards)

| Date | Submission | pub = priv | ref |
|------|-----------|-----------|-----|
| 2026-08-28 | **deputy v3 — frontier single-note (peak)** | **26.520** | 55834276 |
| 2026-08-29 | deputy farm roll 2 | 26.355 | 55861384 |
| 2026-08-30 | deputy farm roll 4 | 26.175 | 55889868 |
| 2026-08-30 | deputy farm roll 8 | 26.025 | 55890039 |
| 2026-08-26 | deputy v2 test submit | 21.525 | 55781871 |

### Abandoned experiments (kept for history)

| Submission | pub | note |
|-----------|-----|------|
| combo v1 (http.post exfil + email.send note) | 44.495 | out-scored by pure exfil on public; superseded |

## Engine → file mapping

| Engine | File | Role |
|--------|------|------|
| `email.send` confused deputy (26.52) | `attack_private.py` | **medal engine** — embedded in `submission_notebook.ipynb` |
| `http.post` exfil v8 (multipost-off) | `attack.py` | public-board representative (V19 lineage) |
| adaptive throughput-first (historic) | `experiments/paste_this_cell.py` | early unified engine, superseded |
