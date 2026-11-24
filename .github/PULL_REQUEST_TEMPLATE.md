<!-- Lock360 PR template — keep it short, keep it RTL-safe (no Markdown tables), keep it secret-free. -->

## What / ماذا يغيّر هذا الطلب؟

<!-- One or two lines. سطر أو سطران. -->

## Why / لماذا؟ (the gap it closes — الفجوة التي يسدّها)

<!-- Link the issue or describe the real-world gap (stage 3.x / gear P-S-M-L). -->

## Blast radius / نطاق الأثر

- Files touched:
- Existing behaviour that must keep working:

## Verification checklist / قائمة التحقق

- [ ] `python3 scripts/verify_repo.py` passes locally (all checks `PASS`, zero `FAIL`).
- [ ] If tracked files changed: ran `python3 scripts/verify_repo.py --update-manifest` and committed the refreshed `MANIFEST.sha256`.
- [ ] `RTL-Safe`: no Markdown tables (`| col |`) added to Arabic-facing core or docs; vertical cards and bullet lists only.
- [ ] No secrets, tokens, API keys, or personal machine paths (absolute Windows user-profile paths, `/home/<name>/...`) anywhere in the diff; use `~/...` or `%USERPROFILE%` instead.
- [ ] Version mentions (`vMAJOR.MINOR`) stay consistent with `VERSION`; `gist/04-CHANGELOG.md` updated if user-facing behaviour changed.
- [ ] Installers (`scripts/install.ps1` / `scripts/install.sh`) still install and uninstall cleanly if touched (CI runs both round-trips).
- [ ] No temporary or test files left in the repository.

## Evidence / الدليل القاطع

<!-- Paste the verifier summary line, e.g. `SUMMARY: PASS=12 FAIL=0 SKIP=0`, or CI link. -->
