# Verification record

## Executed

- `python3 scripts/validate.py`: unique entries, all attachment IDs and older import IDs, promotion aliases, all classifications, unique category counts, 500+ distinct teaching combinations, required lesson fields, bilingual guided examples and unit sizes.
- `node tests/qa.cjs`: adapted original legacy checks covering 12 screens, source quote budgets, internal bands, quizzes, all five card tabs, family/collocation panels, writing, speaking timer, assistance, expression practice, unit scope, sentence notebook, audio preferences and actual backup restore.
- `node tests/revision.cjs`: compact cold startup, shared resolver across topic/cards/review, 500+ registered senses, wrong→correct same-day scheduling, no repeated interval growth, assisted handling, legacy migration, draft/backup round trips, every stable source ID, categories, combined filters, named family corrections, 15 routes, failed download retry, recording/permission mocks, expression-sense review, corruption recovery and conflicting-tab writes.
- `node tests/offline.cjs`: service-worker logic with mocked caches/network; essential versus optional files, scope-specific cleanup, optional-pack failure, offline document/navigation responses.
- JavaScript syntax checks for all runtime modules and retained scripts.

These DOM tests use mocked elements, not a rendering engine. Recording tests use a MediaRecorder stub. Offline tests do not certify the real install/update lifecycle.

## Browser/device limitation

Playwright is installed, but launching Chromium failed because this environment contains no installed browser executable. No desktop/mobile screenshots, screen-reader run, physical-device audio test, zoom/reflow rendering, computed contrast audit or end-to-end service-worker update test was performed. WCAG 2.2 AA is a target, not a verified compliance statement. Manually test keyboard focus, Escape/close restoration, light/dark contrast, 200%/400% zoom, Urdu mixed punctuation, narrow screens, microphone denial, recording playback and installed offline updates before broad release.

## Loading measurement

`baseline.json` measures the raw sizes of initially requested source JSON in the attached edition. `verified-inventory.json` measures the revised course startup payload. These are byte counts, not measured network latency or user-device responsiveness. Optional pack timings and search latency must still be tested on a low-end phone. No worker search was added without that evidence.

## Editorial limitation

See `docs/editorial-and-pilot.md`. This is a functioning repository update, not an independently certified review of every inherited source record. The 200 topic examples still need Urdu sentence translations, all senses need independently checked delayed-context coverage, and some unit reading/model material remains a scaffold. The inherited family bank remains a reference collection outside the specifically corrected entries.
