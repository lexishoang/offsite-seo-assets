#!/usr/bin/env python3
"""Render all visuals for one article and place them in its Markdown.

Usage: python3 make_visuals.py ARTICLE.md OUT_DIR

ARTICLE.md has YAML frontmatter (see references/writing-brief.md) plus a `visuals:` block:

visuals:
  cover:   {variant: light, shot: files_chat}      # variant light (UI crop) | type (no UI)
  figure:  {type: decision|steps|versus, anchor: "<exact H2 text>", title: "...", rows|steps|left/right: ...}
  product: {anchor: "<exact H2 text>", shot: files|files_chat|tasks|meeting|admin, title: "..."}

Every markdown table in the body becomes a branded table image.
Writes OUT_DIR/<platform>-<slug>-{cover,figure,product,tableN}.png, OUT_DIR/<slug>.md
(images referenced by file name, in place) and OUT_DIR/<slug>.json (image list).
No Drumee logo is drawn on any of these: they go on third-party blogs.
"""
import json, os, re, sys
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import brand as B

SIZES = {"devto": (1000, 420), "medium": (1400, 788), "hashnode": (1600, 840), "quora": (1400, 788)}
UI_RE = re.compile(r"^\[\[(UI|SCREENSHOT):.*\]\]\s*$")


def strip_md(c):
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", c).replace("**", "")


def main(src, out):
    os.makedirs(out, exist_ok=True)
    raw = open(src).read()
    _, fm, body = raw.split("---", 2)
    fm = yaml.safe_load(fm); body = body.strip()
    slug, pl = fm["slug"], fm["platform"]
    vis = fm.get("visuals", {})
    pre = os.path.join(out, f"{pl}-{slug}")
    images = []

    if pl != "quora":
        cv = vis.get("cover", {"variant": "type"})
        w, h = SIZES[pl]
        B.cover3(f"c-{slug}", pre + "-cover.png", w, h, fm["cover_line1"], fm["cover_line2"], fm.get("cover_kicker", ""),
                 shot=cv.get("shot"), variant=cv.get("variant", "light" if cv.get("shot") else "type"))
        images.append({"key": "cover", "file": os.path.basename(pre + "-cover.png"), "alt": "Cover: " + fm["title"]})

    after = {}
    fg = vis.get("figure")
    if fg:
        f = pre + "-figure.png"
        if fg["type"] == "decision":
            B.fig_decision(f"f-{slug}", f, fg["title"], fg["rows"])
        elif fg["type"] == "steps":
            B.fig_steps(f"f-{slug}", f, fg["title"], fg["steps"])
        else:
            B.fig_versus(f"f-{slug}", f, fg["title"], fg["left"], fg["right"])
        images.append({"key": "figure", "file": os.path.basename(f), "alt": fg["title"]})
        after.setdefault(fg["anchor"].strip(), []).append("figure")
    pr = vis.get("product")
    if pr:
        f = pre + "-product.png"
        B.fig_product3(f"p-{slug}", f, pr["shot"], pr["title"])
        images.append({"key": "product", "file": os.path.basename(f), "alt": pr["title"]})
        after.setdefault(pr["anchor"].strip(), []).append("product")

    alt = {i["key"]: i for i in images}
    lines, outl, i, n_tab, placed = body.splitlines(), [], 0, 0, set()
    while i < len(lines):
        s = lines[i].strip()
        if UI_RE.match(s):
            i += 1; continue
        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append([strip_md(c) for c in cells])
                i += 1
            n_tab += 1
            f = f"{pre}-table{n_tab}.png"
            B.table(f"t-{slug}-{n_tab}", f, rows[0], rows[1:])
            key = f"table{n_tab}"
            alt[key] = {"key": key, "file": os.path.basename(f), "alt": "Comparison: " + ", ".join(r[0] for r in rows[1:])}
            images.append(alt[key])
            outl += [f"{{{{IMG:{key}}}}}", ""]
            continue
        outl.append(lines[i])
        m = re.match(r"^##\s+(.*)", s)
        if m and m.group(1).strip() in after:
            j = i + 1; buf = []
            while j < len(lines) and not lines[j].strip():
                j += 1
            while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith(("#", "|", "[[", "-", "1.")):
                buf.append(lines[j]); j += 1
            if buf:
                outl += [""] + buf; i = j - 1
            for k in after[m.group(1).strip()]:
                outl += ["", f"{{{{IMG:{k}}}}}", ""]; placed.add(k)
        i += 1
    for k in [k for v in after.values() for k in v if k not in placed]:
        print(f"! anchor not found for {k}; check the H2 text", file=sys.stderr)

    B.run_jobs()
    md = re.sub(r"\{\{IMG:([^}]+)\}\}", lambda m: f"![{alt[m.group(1)]['alt']}]({alt[m.group(1)]['file']})", "\n".join(outl))
    open(os.path.join(out, f"{slug}.md"), "w").write(md.strip() + "\n")
    json.dump({"slug": slug, "platform": pl, "title": fm["title"], "subtitle": fm.get("subtitle", ""), "tags": fm.get("tags", []),
               "meta_description": fm.get("meta_description", ""), "images": images}, open(os.path.join(out, f"{slug}.json"), "w"), indent=1)
    print("ok", slug, len(images), "images")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
