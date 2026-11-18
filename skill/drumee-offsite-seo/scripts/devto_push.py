#!/usr/bin/env python3
"""Publish an article's images to the public image repo and create/update its Dev.to DRAFT.

Usage: python3 devto_push.py OUT_DIR SLUG [--repo /home/user/offsite-seo-assets] [--id DEVTO_ARTICLE_ID]

- Copies OUT_DIR/devto-SLUG-*.png into <repo>/devto/SLUG/, commits and pushes (git must be set up).
- Rewrites image links in OUT_DIR/SLUG.md to raw.githubusercontent.com URLs.
- Creates (or with --id updates) the Dev.to article with published=false and main_image = cover.
Needs env var `devto` (Dev.to API key). Never publishes: the user airs posts themselves.
"""
import argparse, json, os, re, shutil, subprocess, time
import requests

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("slug")
ap.add_argument("--repo", default="/home/user/offsite-seo-assets")
ap.add_argument("--owner", default="lexishoang/offsite-seo-assets")
ap.add_argument("--id", type=int)
a = ap.parse_args()

meta = json.load(open(os.path.join(a.out, f"{a.slug}.json")))
dest = os.path.join(a.repo, "devto", a.slug)
os.makedirs(dest, exist_ok=True)
names = {}
for im in meta["images"]:
    short = im["file"].replace(f"devto-{a.slug}-", "")
    shutil.copy(os.path.join(a.out, im["file"]), os.path.join(dest, short))
    names[im["file"]] = short
subprocess.run(["git", "-C", a.repo, "add", "-A"], check=True)
subprocess.run(["git", "-C", a.repo, "-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com", "commit", "-qm",
                f"Add Dev.to images for {a.slug}"], check=False)
subprocess.run(["git", "-C", a.repo, "-c", "push.negotiate=true", "push", "-q", "origin", "HEAD"], check=True)
raw = f"https://raw.githubusercontent.com/{a.owner}/main/devto/{a.slug}/"
for _ in range(10):  # wait until raw URLs serve
    if requests.get(raw + "cover.png", timeout=20).status_code == 200:
        break
    time.sleep(6)

md = open(os.path.join(a.out, f"{a.slug}.md")).read()
md = re.sub(r"\]\(([^)\s]+\.png)\)", lambda m: f"]({raw}{names.get(m.group(1), m.group(1))})", md)
art = {"title": meta["title"], "body_markdown": md, "published": False, "description": meta["subtitle"][:250],
       "tags": [re.sub(r"[^a-z0-9]", "", t.lower()) for t in meta["tags"]][:4], "main_image": raw + "cover.png"}
hdr = {"api-key": os.environ["devto"], "Content-Type": "application/json", "Accept": "application/vnd.forem.api-v1+json"}
url = f"https://dev.to/api/articles/{a.id}" if a.id else "https://dev.to/api/articles"
for attempt in range(4):
    r = (requests.put if a.id else requests.post)(url, headers=hdr, json={"article": art}, timeout=60)
    if r.status_code != 429:
        break
    time.sleep(35 * (attempt + 1))
r.raise_for_status()
d = r.json()
print(json.dumps({"id": d.get("id"), "edit_url": d.get("url", "") + "/edit", "published": d.get("published")}))
