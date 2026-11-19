---
name: drumee-offsite-seo
description: Weekly off-site SEO content for Drumee on third-party platforms (Dev.to, Medium, Hashnode, Quora) and listing sites (Product Hunt, AlternativeTo, SaaSHub, G2, Capterra, awesome-selfhosted, OpenAlternative). Writes independent-blogger-style comparison articles around "X alternative" keywords, renders clean branded visuals from real Drumee 2.0 screenshots (no Drumee logo on third-party posts), pushes Dev.to drafts with images, and adds ready-to-paste tabs to the "Drumee Offsite SEO – Ready to post" doc. Use this whenever the user asks for offsite SEO, backlink or third-party blog posts, Dev.to / Medium / Hashnode / Quora content, "bài offsite", "bài third party", the weekly offsite batch, listing-site copy, or wants more posts to air during the week, even if they don't say "skill" or name a platform.
---

# Drumee offsite SEO

Produce third-party content that earns Drumee referral traffic, brand mentions and AI-search citations without reading like an ad. The user (Triều/Lexis, Drumee growth) reads Vietnamese; all post copy is English.

## What a weekly batch contains

Default batch (the user airs one article per weekday and does the posting/scheduling themselves):
- **5 articles**: 2 Dev.to + 3 split between Medium and Hashnode (alternate 2+1 / 1+2 each week).
- **5 Quora answers** (one per day).
- Each article = cover + comparison table image + one figure (decision / steps / versus) + one product shot.
Never publish anything on any platform. Dev.to posts are created as drafts; everything else goes into the doc for copy-paste.

## Fixed resources

- Doc: https://claude.ai/artifact/FJnP1cduxNSKqiTiJ5Mhqz ("Drumee Offsite SEO – Ready to post"). Read `references/doc-format.md` before adding tabs.
- Dev.to: account `drumee`, API key in env var `devto`. Forem API has no image upload, so images go to the public repo below first.
- Image repo: `lexishoang/offsite-seo-assets` (public, push access). Attach with add_repo if needed, clone to `/home/user/offsite-seo-assets`.
- Hashnode API is paid (Pro) since May 2026 → Hashnode is copy-paste from the doc. Medium has no API → same.
- Keyword backlog: `references/keywords.md` (move used ones to "Used"; when < 8 remain, research and add 10 new ones around EU / self-hosted / collaboration intent).

## Tracking links and the $1 campaign

Every Drumee link in a post must be the tracking link for its platform, so sign-ups can be attributed. Read `references/tracking.md` before writing: it has the exact URLs, the offer line to place just above the disclosure, and the date the campaign ends.

## Workflow

1. **Pick topics** from the keyword backlog. Never repeat a topic already written (check the doc's tab names too).
2. **Write** with subagents in parallel, one per piece, giving each the full `references/writing-brief.md` plus its topic, platform and slug. The brief carries the rules that matter most: verified facts with primary-source links, Drumee as one fair option (usually not first) with honest trade-offs, first-person + disclosure on Medium/Hashnode/Quora, neutral voice on Dev.to, tracking links from `references/tracking.md` (including the offer line while the campaign runs), banned claims. Drumee 2.0 task views include board, list, backlog, calendar, timeline and reports, so never write that Drumee lacks Gantt/timeline/reports; say task planning is lighter than a dedicated PM tool instead.
3. **Add a `visuals:` block** to each article's frontmatter (format in `scripts/make_visuals.py` docstring and `references/visual-system.md`): pick the cover variant and screenshot that match the topic, write the figure from the article's own content (no new facts), and anchor the figure and product shot to exact H2 headings.
4. **Render**: `python3 scripts/make_visuals.py article.md OUTDIR` per article. Then *look at every PNG* (Read the file). Fix anything that overlaps, truncates or looks empty before moving on: a quick look catches most problems, and a bad image costs more than the minute it takes.
5. **Dev.to**: `python3 scripts/devto_push.py OUTDIR SLUG` → pushes images to the repo and creates the draft with cover and inline images. Record the edit URL.
6. **Doc**: upload images to the doc artifact (Artifact publish with `asset: true`, `file_paths` batches of ≤25, files must live under the working directory), create blobs, then add one tab per piece following `references/doc-format.md`. Name tabs `Week <dd/mm> · <Mon..Fri> · <Platform> · <topic>` and one `Week <dd/mm> · Quora (5 answers, 1/day)`; add the week's air plan to the Start here tab.
7. **Report** to the user in Vietnamese, short: the air plan (day → tab), Dev.to draft links, anything to check (claims the writers flagged as unverifiable, screenshots, prices).

## Visual rules (why they exist)

- **No Drumee logo on third-party article visuals.** These sit on independent-looking posts; a logo turns them into ads. Listing-site gallery images (Product Hunt, G2…) do carry the logo, because those pages are Drumee's own.
- **Readable UI or no UI.** The old versions shrank whole-app screenshots until nothing was legible. The v3 templates crop a relevant region of a real Drumee 2.0 screenshot and annotate it with numbered markers. Use `cover3` (variant `light` with a shot, or `type` for abstract topics like licences/GDPR) and `fig_product3`.
- Brand: Geist 800 titles, second line purple, #433CC5 ≥30% of the canvas, flat backgrounds, no 3D/stock/mascots, no competitor logos (competitor names in text are fine for SEO). Details in `references/visual-system.md`.
- Screenshots come from a demo workspace (Acme Inc., fake names). If the user sends new ones, add them to `scripts/ui2/` and register crop boxes and marker points in `SHOT3` in `brand.py`.

## Listing sites

Submission copy and rules live in the doc's "Listing sites" tab. awesome-selfhosted bans AI-written contributions: give facts and rules only; a person writes and submits. SaaSHub asks for human submitters. Capterra now runs through G2's form.
