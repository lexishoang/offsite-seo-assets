# Visual system for third-party posts

All templates live in `scripts/brand.py` and render with Playwright via `scripts/render.js` (Chromium is preinstalled in cloud sessions; `require('playwright')` works).

## Sizes
| Platform | Cover |
| --- | --- |
| Dev.to | 1000×420 (rendered at 2x) |
| Medium | 1400×788 |
| Hashnode | 1600×840 |
In-article figures: 1600×900; tables: 1400 wide, auto height.

## Templates
- `cover3(name, out, w, h, line1, line2, kicker, shot=None, variant="light"|"type")`: light = white left with title, purple panel right holding a flat, zoomed UI crop; type = solid #433CC5 with large title and rings, no UI. Use `type` for abstract topics (licences, GDPR, sovereignty) and `light` when a screenshot shows the topic. Lines ≤24 chars, kicker ≤20.
- `fig_product3(name, out, shot, title)`: purple left column with title + numbered legend, zoomed crop with numbered markers on the right. Title ≤48 chars.
- `fig_decision(name, out, title, rows)`: 3–5 rows `[condition ≤55, pick ≤28]`.
- `fig_steps(name, out, title, steps)`: 3–4 `[title ≤28, line ≤70]`.
- `fig_versus(name, out, title, left, right)`: `{"label": ≤28, "items": [≤45 ×3–4]}`; right side = the connected-workspace side, left side shows real strengths.
- `table(name, out, header, rows)`: ≤6 rows, ≤4 columns, short cells.

## Screenshots (`SHOT3` in brand.py)
| shot | shows | markers |
| --- | --- | --- |
| files_chat | topics, file threads, live meeting card in chat | file threads, meeting card, open thread |
| tasks | board with views tabs, linked files, subtasks | views, linked files, subtasks |
| files | file list grouped by type, locked files, filters | grouping, lock, filters |
| meeting | in-call chat next to a video tile | in-call chat, reactions, share files |
| admin | org manage grid: members, requests, security, audit log | members, requests, 2-step |
To add a screenshot: save to `scripts/ui2/`, add an entry with `box` (crop in source px) and `pts` (marker x, y, label in source px, placed on empty space next to the element, not on its text). Render and look.

## Checks before using an image
- No text overlaps or is cut off; markers sit beside, not on, labels.
- No real faces or real emails (meeting crops avoid face tiles).
- No Drumee logo on article visuals; competitor names only as text.
