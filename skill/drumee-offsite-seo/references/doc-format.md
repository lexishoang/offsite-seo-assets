# Doc tab format ("Drumee Offsite SEO – Ready to post")

Doc id `73db8d2a-e9d1-4d3c-8aad-eaadfb4b21f9`, link https://claude.ai/artifact/FJnP1cduxNSKqiTiJ5Mhqz.
Load the docs guide first (`guide(["topic.index"])`, plus `topic.uploads`, `topic.tabs`). The user reads and copies from this doc, so keep it plain and consistent.

## Images
1. Copy PNGs under the working directory, upload with Artifact publish `asset: true` + `file_paths` (≤25 per call).
2. `batch` of `{"verb":"create","object":"blob","engine":"blob","payload":{"asset":"<id>"}}` → minted ids; reference as `![alt](blob/<minted>)`.

## One tab per article (one `batch`: create file, create prose node, point file to node, set tabs order/name)
```
# <Title>

**Cách đăng (<Platform>, tài khoản cá nhân):** <2–4 short Vietnamese steps for that platform>

| Field | Paste this |
| --- | --- |
| Title | … |
| Subtitle | … |
| Tags | … |
| SEO title | … |
| SEO description | … |
| Target keyword | … |
| Air day | Thứ Hai … |

## Cover
![Cover](blob/…)

## Body: copy từ đây xuống cuối
<article body, article H2→###, H3→####, images in place>
```
Dev.to tabs: replace the field table with Draft link (`<url>/edit`), Title, Tags, Air day, and the instruction "draft đã có đủ chữ, cover và ảnh; mở draft, Preview, Publish".

Steps per platform:
- Medium: Write → paste title, subtitle, body → re-insert any image that didn't paste → Publish, 5 tags → Story settings → SEO title/description.
- Hashnode: New draft → Add cover → paste title/subtitle/body → Draft settings: tags, SEO, leave "originally published" empty → Publish.
- Quora: personal account, 1 answer/day, search the question (ask it yourself if missing), keep the disclosure, add "Works at Drumee" to the profile.

Tab order keys: existing tabs use a0, b01–b05, c01–c03, d01–d03, e01, f01. New weeks use `w<yymmdd>-<n>` so they sort after.
