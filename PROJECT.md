# getfactormodels — sackio fork

Canonical task list for this project. ⛔ Not the pin, not Slack: this file is the list, and
the build contradicts it when it is wrong.

**DONE means:** all 15 models pull, each is asserted in a vbt example notebook, and the whole
`vectorbt.pro/examples/` set passes the weekly gate against this fork installed in
`vbt-env:latest`.

- upstream `x512/getfactormodels` (AGPL-3.0) · ours `sackio/getfactormodels` (public fork)
- working branch `work`
- vbt examples land in `/mnt/nas/data/code/forks/vectorbt.pro/examples/`

---

## 1 · Make it work

⭐ 2026-09-04: suite green, 42 pass / 0 fail, from a 39/3 baseline. Root cause was one upstream
commit, 6cbb0a9 "clean up http client", which deleted four behaviours its own tests still assert.
Restored in our `work` branch — a candidate to offer upstream.

- [x] `tests/test_http.py::test_http_error_when_used_outside_context` — fails on a clean
      checkout (baseline 2026-09-04: 39 pass, 3 fail)
- [x] `tests/test_http.py::test_download_with_http_client` — same
- [x] `tests/test_http.py::test_check_connection_fallback_to_get` — same
- [ ] `model=5` as an int raises `AttributeError: 'int' object has no attribute 'startswith'`
      while the constructor advertises `model: int | str`. Pass `model="5"` today.
- [ ] decide, per model, what a smoke test asserts — every one of the 15 must pull

## 2 · Bake it in

- [ ] requirements group in `vectorbt.pro/scripts/requirements/`, installed from our fork
- [ ] `check_vbt_env.py` exercises it — FIT a model, do not merely import (the rule earned
      by lightgbm: a wheel that unpacked is not a shared object that links)
- [ ] candidate tag, full gate green on that digest, then move `:latest`

## 3 · vbt examples

One notebook per mechanism, not per model. Candidates, each needing its own measurement first:

- [ ] the coverage cliff — series end anywhere from 2016-12 to 2026-06, and a factor set that
      stops in 2016 regresses happily against returns through 2026 and silently drops rows
- [ ] what a factor model does to `Portfolio.from_signals` — alpha vs the raw return
- [ ] the models disagree: same asset, same window, different factor set, different residual

## Measured facts (2026-09-04)

Per-model currency, pulled from the installed package:

| model | latest |
|---|---|
| Fama-French 3/5/6, Carhart | 2026-06 |
| ICR | 2025-05 |
| q5, Pastor-Stambaugh liquidity | 2024-12 |
| DHS | 2023-12 |
| Stambaugh-Yuan mispricing | 2016-12 |

⛔ Author marks the package `Development Status :: 2 - Pre-Alpha` and the README says
"don't rely on it for anything". That is why §2 gates on a full green gate, not on an import.
