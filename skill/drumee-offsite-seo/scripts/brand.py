"""Drumee brand visual templates -> HTML (rendered to PNG by render.js).

Brand rules applied: Geist 800 titles with negative tracking, second title line
in purple (gradient #433CC5 -> #5950FF on light, white 80% on dark), purple
>= 30% of the canvas, full Drumee logo top-left (brand pieces), UI in window
cards (3 dots, radius 16, soft shadow, slight tilt), fades by mask only,
backgrounds: flat #433CC5 (A), #433CC5 + #9590FF glow top-right (B), or
white -> #F4F3FF (light). Never a #5950FF background gradient.
"""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
import tempfile
HTML_DIR = os.environ.get("OFFSITE_HTML_DIR") or tempfile.mkdtemp(prefix="offsite-html-")
os.makedirs(HTML_DIR, exist_ok=True)
JOBS = []

BASE_CSS = """
@font-face{font-family:Geist;src:url(__FONT__) format('woff2');font-weight:100 900;}
:root{--p:#433CC5;--p2:#5950FF;--pl:#9590FF;--bgl:#F4F3FF;--bd:#DEDEE8;--t1:#0F1011;--t2:#3E3D5C;--t3:#5B5A7A;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Geist,system-ui,sans-serif;background:#fff;-webkit-font-smoothing:antialiased}
.stage{position:relative;overflow:hidden}
.bgA{background:#433CC5}
.bgB{background:radial-gradient(140% 110% at 100% 0%,#9590FF 0%,rgba(149,144,255,.6) 28%,transparent 70%),#433CC5}
.bgL{background:linear-gradient(135deg,#FFFFFF 0%,#F4F3FF 100%)}
.title{font-weight:800;letter-spacing:-0.035em;line-height:1.02;white-space:nowrap}.title>div{width:max-content;padding-right:.04em}
.dark .l1{color:#fff}.dark .l2{color:rgba(255,255,255,.8)}
.light .l1{color:var(--t1)}
.light .l2{background:linear-gradient(90deg,#433CC5,#5950FF);-webkit-background-clip:text;background-clip:text;color:transparent}
.kicker{font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.dark .kicker{color:rgba(255,255,255,.72)}.light .kicker{color:var(--p)}
.win{position:absolute;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 30px 80px -20px rgba(15,16,17,.35),0 8px 24px -8px rgba(15,16,17,.18);border:1px solid var(--bd)}
.win .bar{height:34px;background:#fff;border-bottom:1px solid var(--bd);display:flex;align-items:center;gap:8px;padding:0 14px}
.win .bar i{width:11px;height:11px;border-radius:50%;background:#DEDEE8;display:block}
.win img{display:block;width:100%}
.rings{position:absolute;border-radius:50%;border:1.5px solid rgba(255,255,255,.12)}
.dots{position:absolute;display:grid;gap:14px}
.dots b{width:5px;height:5px;border-radius:50%;background:rgba(255,255,255,.4);display:block}
.infobar{position:absolute;display:flex;align-items:center;gap:14px;border-radius:999px;font-weight:600}
.dark .infobar{background:rgba(255,255,255,.12);color:#fff}
.light .infobar{background:#fff;color:var(--t2);border:1px solid var(--bd)}
"""

FIT_JS = """
<script>
document.fonts.ready.then(()=>{document.querySelectorAll('[data-fit]').forEach(el=>{
  const max=parseFloat(el.dataset.fit);let s=parseFloat(getComputedStyle(el).fontSize);
  while(s>12&&[...el.children].some(c=>c.getBoundingClientRect().width>max)){s-=1;el.style.fontSize=s+'px';}
});});
</script>"""


def esc(s):
    return html.escape(s or "")


def rel(p):
    return "file://" + os.path.abspath(p)


def rings(cx, cy, base, n=4, step=None):
    step = step or base * 0.45
    return "".join(
        f'<div class="rings" style="width:{base+2*i*step}px;height:{base+2*i*step}px;left:{cx-(base/2+i*step)}px;top:{cy-(base/2+i*step)}px"></div>'
        for i in range(n))


def dots(x, y, cols=6, rows=4):
    return f'<div class="dots" style="left:{x}px;top:{y}px;grid-template-columns:repeat({cols},5px)">' + "<b></b>" * (cols * rows) + "</div>"


def window(img, style, bar=True, fade=False):
    mask = "-webkit-mask-image:linear-gradient(to bottom,#000 72%,transparent 100%);mask-image:linear-gradient(to bottom,#000 72%,transparent 100%);" if fade else ""
    b = '<div class="bar"><i></i><i></i><i></i></div>' if bar else ""
    return f'<div class="win" style="{style}{mask}">{b}<img src="{rel(img)}"></div>'


def page(name, w, h, body, extra_css="", auto=False):
    hstyle = "" if auto else f"height:{h}px;"
    css = BASE_CSS.replace("__FONT__", rel(os.path.join(HERE, "fonts", "Geist.woff2")))
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}{extra_css}</style></head>
<body><div class="stage" style="width:{w}px;{hstyle}">{body}</div>{FIT_JS}</body></html>"""
    p = os.path.join(HTML_DIR, name + ".html")
    open(p, "w").write(doc)
    return p


def job(html_path, out, w, h, scale=1):
    JOBS.append({"html": html_path, "out": out, "w": w, "h": h, "scale": scale})


# ---------------------------------------------------------------- covers
def cover(name, out, w, h, kind, l1, l2, kicker="", ui=None, brand=True, scale=1):
    """kind: A | B (dark) or L (light)."""
    dark = kind in ("A", "B")
    pad = round(h * 0.09)
    logo_h = round(h * 0.065)
    logo = ""
    if brand:
        logo = f'<img src="{rel(os.path.join(HERE, "logo-white.svg" if dark else "logo-dark.svg"))}" style="position:absolute;left:{pad}px;top:{pad}px;height:{logo_h}px">'
    text_w = round(w * ((0.50 if dark else 0.45) if ui else 0.62))
    fs = round(h * 0.125)
    ks = max(13, round(h * 0.03))
    top_txt = pad + (logo_h + round(h * 0.09) if brand else round(h * 0.04))
    kick = f'<div class="kicker" style="font-size:{ks}px;margin-bottom:{round(h*0.035)}px">{esc(kicker)}</div>' if kicker else ""
    title = (f'<div style="position:absolute;left:{pad}px;top:{top_txt}px;width:{text_w}px">{kick}'
             f'<div class="title" data-fit="{text_w}" style="font-size:{fs}px"><div class="l1">{esc(l1)}</div><div class="l2">{esc(l2)}</div></div></div>')
    deco, vis = "", ""
    if dark:
        deco = rings(w * 0.92, h * 0.05, h * 0.35, 5) + dots(round(w * 0.70), round(h * 0.08))
        if ui:
            vis = window(ui, f"width:{round(w*0.46)}px;right:{-round(w*0.03)}px;top:{round(h*0.30)}px;transform:rotate(-4deg);", fade=True)
    else:
        panel = f'<div style="position:absolute;right:0;top:0;bottom:0;width:{round(w*0.40)}px;background:#433CC5;border-radius:{round(h*0.06)}px 0 0 {round(h*0.06)}px;overflow:hidden">' \
                + rings(w * 0.40, 0, h * 0.4, 4) + "</div>"
        deco = panel
        if ui:
            vis = window(ui, f"width:{round(w*0.44)}px;right:{round(w*0.05)}px;top:{round(h*0.20)}px;transform:rotate(3deg);")
        else:
            deco = f'<div style="position:absolute;right:0;top:0;bottom:0;width:{round(w*0.30)}px;background:#433CC5;overflow:hidden">' + rings(w * 0.30, h * 0.5, h * 0.3, 5) + "</div>"
    bar = ""
    if brand:
        bs = max(12, round(h * 0.028))
        bar = f'<div class="infobar" style="left:{pad}px;bottom:{round(pad*0.8)}px;font-size:{bs}px;padding:{round(bs*0.6)}px {round(bs*1.1)}px">drumee.com · Files · Chat · Tasks · Meet</div>'
    body = f'<div class="{"dark bg"+kind if dark else "light bgL"}" style="position:absolute;inset:0">{deco}{vis}{logo}{title}{bar}</div>'
    job(page(name, w, h, body), out, w, h, scale)


# ---------------------------------------------------------------- tables
def table(name, out, header, rows, title="", w=1400, scale=1):
    th = "".join(f"<th>{esc(c)}</th>" for c in header)
    tr = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows)
    ttl = f'<div class="tt">{esc(title)}</div>' if title else ""
    css = """
    .wrap{padding:56px 56px 64px;position:relative}
    .tt{color:#fff;font-weight:800;font-size:34px;letter-spacing:-.03em;margin:0 0 26px 4px;position:relative}
    .card{position:relative;background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 24px 60px -24px rgba(15,16,17,.45)}
    table{width:100%;border-collapse:collapse;font-size:22px}
    th{background:#F4F3FF;color:#433CC5;text-align:left;font-weight:700;padding:20px 24px;border-bottom:1px solid #DEDEE8;letter-spacing:-.01em}
    td{padding:18px 24px;color:#3E3D5C;border-bottom:1px solid #EEEEF4;vertical-align:top;line-height:1.35}
    tr:last-child td{border-bottom:none}
    td:first-child{font-weight:700;color:#0F1011}
    tr:nth-child(even) td{background:#FBFBFF}
    """
    body = f'<div class="dark bgA wrap">{rings(w-40, 10, 220, 4)}{dots(w-330, 40)}{ttl}<div class="card"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div></div>'
    job(page(name, w, 0, body, css, auto=True), out, w, "auto", scale)


# ---------------------------------------------------------------- UI frame for articles
def uiframe(name, out, img, w=1400, scale=1):
    css = ".wrap{padding:64px 72px 72px;position:relative}"
    body = (f'<div class="light bgL wrap"><div style="position:absolute;right:0;bottom:0;width:46%;height:62%;background:#433CC5;border-radius:28px 0 0 0;overflow:hidden">{rings(w*0.46, 0, 260, 4)}</div>'
            f'<div class="win" style="position:relative">'
            f'<div class="bar"><i></i><i></i><i></i></div><img src="{rel(img)}"></div></div>')
    job(page(name, w, 0, body, css, auto=True), out, w, "auto", scale)


def run_jobs(path=None):
    path = path or os.path.join(HTML_DIR, "jobs.json")
    json.dump(JOBS, open(path, "w"), indent=1)
    os.system(f"node {os.path.join(HERE, 'render.js')} {path}")
    JOBS.clear()


# ---------------------------------------------------------------- listing gallery
def _sub(text, dark, size):
    col = "rgba(255,255,255,.78)" if dark else "#3E3D5C"
    return f'<div style="margin-top:{round(size*1.1)}px;font-size:{size}px;line-height:1.4;color:{col};font-weight:500;white-space:normal">{esc(text)}</div>'


def slide_hero(name, out, w, h, kind, l1, l2, sub, ui, kicker=""):
    """Gallery slide: logo, title, subline, UI window. kind A/B/L."""
    dark = kind in ("A", "B")
    pad = round(h * 0.08); logo_h = round(h * 0.06)
    text_w = round(w * (0.44 if dark else 0.37))
    fs = round(h * 0.085)
    logo = f'<img src="{rel(os.path.join(HERE, "logo-white.svg" if dark else "logo-dark.svg"))}" style="position:absolute;left:{pad}px;top:{pad}px;height:{logo_h}px">'
    kick = f'<div class="kicker" style="font-size:{round(h*0.024)}px;margin-bottom:{round(h*0.03)}px">{esc(kicker)}</div>' if kicker else ""
    title = (f'<div style="position:absolute;left:{pad}px;top:{round(h*0.30)}px;width:{text_w}px">{kick}'
             f'<div class="title" data-fit="{text_w}" style="font-size:{fs}px"><div class="l1">{esc(l1)}</div><div class="l2">{esc(l2)}</div></div>'
             f'{_sub(sub, dark, round(h*0.03))}</div>')
    if dark:
        deco = rings(w * 0.95, h * 0.02, h * 0.35, 5) + dots(round(w * 0.62), round(h * 0.07))
        vis = window(ui, f"width:{round(w*0.52)}px;right:{-round(w*0.04)}px;top:{round(h*0.20)}px;transform:rotate(-3deg);", fade=True)
    else:
        deco = (f'<div style="position:absolute;right:0;top:0;bottom:0;width:{round(w*0.38)}px;background:#433CC5;'
                f'border-radius:{round(h*0.05)}px 0 0 {round(h*0.05)}px;overflow:hidden">' + rings(w * 0.38, 0, h * 0.4, 4) + "</div>")
        vis = window(ui, f"width:{round(w*0.50)}px;right:{round(w*0.04)}px;top:{round(h*0.17)}px;transform:rotate(2.5deg);")
    bs = round(h * 0.022)
    bar = f'<div class="infobar" style="left:{pad}px;bottom:{round(pad*0.8)}px;font-size:{bs}px;padding:{round(bs*0.6)}px {round(bs*1.1)}px">drumee.com · Files · Chat · Tasks · Meet</div>'
    body = f'<div class="{"dark bg"+kind if dark else "light bgL"}" style="position:absolute;inset:0">{deco}{vis}{logo}{title}{bar}</div>'
    job(page(name, w, h, body), out, w, h)


def slide_two_cards(name, out, w, h, l1, l2, cards):
    """Light slide with two option cards. cards=[(label, title, [lines])]."""
    pad = round(h * 0.08); logo_h = round(h * 0.06); fs = round(h * 0.075)
    logo = f'<img src="{rel(os.path.join(HERE, "logo-dark.svg"))}" style="position:absolute;left:{pad}px;top:{pad}px;height:{logo_h}px">'
    title = (f'<div style="position:absolute;left:{pad}px;top:{round(h*0.22)}px;width:{w-2*pad}px">'
             f'<div class="title" data-fit="{w-2*pad}" style="font-size:{fs}px"><div class="l1">{esc(l1)}</div><div class="l2">{esc(l2)}</div></div></div>')
    cw = round((w - 2 * pad - h * 0.04) / 2); top = round(h * 0.52)
    cs = ""
    for i, (lab, t, lines) in enumerate(cards):
        darkc = False
        bg = "#433CC5" if darkc else "#fff"; c1 = "#fff" if darkc else "#0F1011"; c2 = "rgba(255,255,255,.8)" if darkc else "#3E3D5C"
        li = "".join(f'<div style="margin-top:{round(h*0.012)}px">✓&nbsp; {esc(x)}</div>' for x in lines)
        cs += (f'<div style="position:absolute;left:{pad + i*(cw+round(h*0.04))}px;top:{top}px;width:{cw}px;height:{round(h*0.36)}px;background:{bg};'
               f'border-radius:16px;border:1px solid #DEDEE8;padding:{round(h*0.04)}px;box-shadow:0 20px 50px -24px rgba(15,16,17,.35);transform:rotate({-1.5 if i==0 else 1.5}deg)">'
               f'<div class="kicker" style="font-size:{round(h*0.02)}px;color:{"rgba(255,255,255,.7)" if darkc else "#433CC5"}">{esc(lab)}</div>'
               f'<div style="font-weight:800;letter-spacing:-.03em;font-size:{round(h*0.045)}px;color:{c1};margin-top:{round(h*0.015)}px">{esc(t)}</div>'
               f'<div style="font-size:{round(h*0.026)}px;color:{c2};margin-top:{round(h*0.015)}px;font-weight:500">{li}</div></div>')
    band = f'<div style="position:absolute;left:0;right:0;bottom:0;height:{round(h*0.42)}px;background:#433CC5;overflow:hidden">{rings(w*0.9, h*0.42, h*0.3, 5)}</div>'
    body = f'<div class="light bgL" style="position:absolute;inset:0">{band}{logo}{title}{cs}</div>'
    job(page(name, w, h, body), out, w, h)


def slide_end(name, out, w, h, line, chips, kind="B"):
    body = (f'<div class="dark bg{kind}" style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">'
            f'{rings(w*0.5, h*0.5, h*0.5, 5, h*0.12)}'
            f'<img src="{rel(os.path.join(HERE, "logo-white.svg"))}" style="height:{round(h*0.11)}px;position:relative">'
            f'<div style="position:relative;color:#fff;font-weight:800;letter-spacing:-.035em;font-size:{round(h*0.075)}px;margin-top:{round(h*0.06)}px">{esc(line)}</div>'
            f'<div style="position:relative;display:flex;gap:{round(h*0.02)}px;margin-top:{round(h*0.05)}px">'
            + "".join(f'<div class="infobar" style="position:static;font-size:{round(h*0.026)}px;padding:{round(h*0.016)}px {round(h*0.03)}px">{esc(c)}</div>' for c in chips)
            + f'</div><div style="position:relative;color:rgba(255,255,255,.75);font-weight:600;font-size:{round(h*0.028)}px;margin-top:{round(h*0.05)}px">drumee.com</div></div>')
    job(page(name, w, h, body), out, w, h)


def logo_square(name, out, size, bg="#433CC5"):
    mark = "mark-white.svg" if bg != "#fff" else "mark.svg"
    body = f'<div style="position:absolute;inset:0;background:{bg};display:flex;align-items:center;justify-content:center"><img src="{rel(os.path.join(HERE, mark))}" style="width:{round(size*0.62)}px"></div>'
    job(page(name, size, size, body), out, size, size)


def logo_wide(name, out, w, h, dark=False):
    body = f'<div style="position:absolute;inset:0;background:{"#433CC5" if dark else "#fff"};display:flex;align-items:center;justify-content:center"><img src="{rel(os.path.join(HERE, "logo-white.svg" if dark else "logo-dark.svg"))}" style="height:{round(h*0.36)}px"></div>'
    job(page(name, w, h, body), out, w, h)


# ---------------------------------------------------------------- in-article figures (1600x900)
FIG_W, FIG_H = 1600, 900
SHOTS = {"files": "ui2/files.png", "files_chat": "ui2/files_chat.png", "tasks": "ui2/tasks.png",
         "meeting": "ui2/meeting.png", "admin": "ui2/admin_manage.png"}


def _logo(dark, h, style):
    return f'<img src="{rel(os.path.join(HERE, "logo-white.svg" if dark else "logo-dark.svg"))}" style="position:absolute;height:{h}px;{style}">'


def _fig_title(text, dark, x, y, w, size=54):
    col = "#fff" if dark else "#0F1011"
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px"><div class="title" data-fit="{w}" '
            f'style="font-size:{size}px;color:{col}"><div>{esc(text)}</div></div></div>')


def fig_product(name, out, shot, title, callouts, logo=False):
    w, h = FIG_W, FIG_H
    img = os.path.join(HERE, SHOTS[shot])
    chips = "".join(f'<div style="display:flex;align-items:center;gap:12px;background:#fff;border:1px solid #DEDEE8;border-radius:999px;'
                    f'padding:12px 22px;font-size:22px;font-weight:600;color:#3E3D5C;box-shadow:0 6px 18px -10px rgba(15,16,17,.25)">'
                    f'<span style="width:10px;height:10px;border-radius:50%;background:#433CC5;display:block"></span>{esc(c)}</div>' for c in callouts)
    band = f'<div style="position:absolute;left:0;right:0;bottom:0;height:{round(h*0.52)}px;background:#433CC5;overflow:hidden">{rings(w*0.92, h*0.52, 260, 5)}</div>'
    win = window(img, f"width:{round(w*0.80)}px;left:{round(w*0.10)}px;top:{round(h*0.30)}px;", fade=False)
    lg = _logo(False, 40, "right:64px;top:62px") if logo else ""
    body = (f'<div class="light bgL" style="position:absolute;inset:0">{band}{win}{lg}'
            f'{_fig_title(title, False, 64, 52, 1100, 52)}'
            f'<div style="position:absolute;left:64px;top:140px;display:flex;gap:14px">{chips}</div></div>')
    job(page(name, w, h, body), out, w, h)


def fig_decision(name, out, title, rows):
    w, h = FIG_W, FIG_H
    n = len(rows); top = 215; rh = min(160, (h - top - 50) // n)
    rs = ""
    for i, (cond, pick) in enumerate(rows):
        rs += (f'<div style="position:absolute;left:64px;right:64px;top:{top + i*rh}px;height:{rh-22}px;background:#fff;border-radius:16px;'
               f'display:flex;align-items:center;justify-content:space-between;padding:0 36px;box-shadow:0 14px 34px -22px rgba(0,0,0,.5)">'
               f'<div style="font-size:32px;font-weight:500;color:#3E3D5C">{esc(cond)}</div>'
               f'<div style="display:flex;align-items:center;gap:22px"><span style="font-size:30px;color:#9590FF">→</span>'
               f'<div style="background:#F4F3FF;color:#433CC5;border:1.5px solid #DEDEE8;border-radius:12px;padding:12px 24px;font-size:28px;font-weight:800;letter-spacing:-.02em;white-space:nowrap">{esc(pick)}</div></div></div>')
    body = (f'<div class="dark bgA" style="position:absolute;inset:0">{rings(w*0.97, 0, 300, 5)}{dots(1180, 70)}'
            f'<div class="kicker" style="position:absolute;left:64px;top:60px;font-size:20px">Quick decision guide</div>'
            f'{_fig_title(title, True, 64, 96, 1050, 54)}{rs}</div>')
    job(page(name, w, h, body), out, w, h)


def fig_steps(name, out, title, steps):
    w, h = FIG_W, FIG_H
    n = len(steps); gap = 28; cw = (w - 128 - gap * (n - 1)) // n
    cs = ""
    for i, (t, d) in enumerate(steps):
        cs += (f'<div style="position:absolute;left:{64 + i*(cw+gap)}px;top:330px;width:{cw}px;height:420px;background:#fff;border:1px solid #DEDEE8;'
               f'border-radius:18px;padding:40px 34px;box-shadow:0 22px 50px -28px rgba(15,16,17,.45)">'
               f'<div style="width:76px;height:76px;border-radius:16px;background:#433CC5;color:#fff;font-weight:800;font-size:32px;display:flex;align-items:center;justify-content:center;letter-spacing:-.02em">{i+1:02d}</div>'
               f'<div style="margin-top:34px;font-size:{32 if n<4 else 29}px;font-weight:800;letter-spacing:-.03em;color:#0F1011;line-height:1.15">{esc(t)}</div>'
               f'<div style="margin-top:16px;font-size:{25 if n<4 else 23}px;line-height:1.45;color:#3E3D5C;font-weight:500">{esc(d)}</div></div>')
    band = f'<div style="position:absolute;left:0;right:0;bottom:0;height:380px;background:#433CC5;overflow:hidden">{rings(w*0.08, 380, 240, 5)}</div>'
    body = (f'<div class="light bgL" style="position:absolute;inset:0">{band}'
            f'<div class="kicker" style="position:absolute;left:64px;top:84px;font-size:20px">Step by step</div>'
            f'{_fig_title(title, False, 64, 130, 1300, 64)}{cs}</div>')
    job(page(name, w, h, body), out, w, h)


def fig_versus(name, out, title, left, right):
    w, h = FIG_W, FIG_H
    cw = (w - 128 - 40) // 2
    nmax = max(len(left["items"]), len(right["items"]))
    chh = 170 + nmax * 86
    ctop = 250 + max(0, (h - 250 - 60 - chh) // 2)

    def card(x, side, dark):
        bg = "#433CC5" if dark else "#fff"; c1 = "#fff" if dark else "#0F1011"; c2 = "rgba(255,255,255,.88)" if dark else "#3E3D5C"
        mark = "✓" if dark else "•"
        items = "".join(f'<div style="display:flex;gap:16px;margin-top:26px;font-size:30px;line-height:1.35;color:{c2};font-weight:500">'
                        f'<span style="color:{"#fff" if dark else "#433CC5"};font-weight:800;width:22px;flex:none">{mark}</span><span>{esc(it)}</span></div>' for it in side["items"])
        return (f'<div style="position:absolute;left:{x}px;top:{ctop}px;width:{cw}px;height:{chh}px;background:{bg};border-radius:20px;'
                f'border:1px solid {"#433CC5" if dark else "#DEDEE8"};padding:44px 44px;box-shadow:0 26px 60px -30px rgba(15,16,17,.5)">'
                f'<div style="font-size:36px;font-weight:800;letter-spacing:-.03em;color:{c1}">{esc(side["label"])}</div>'
                f'<div style="height:2px;background:{"rgba(255,255,255,.25)" if dark else "#DEDEE8"};margin:26px 0 6px"></div>{items}</div>')
    body = (f'<div class="light bgL" style="position:absolute;inset:0">'
            f'<div style="position:absolute;right:0;top:0;bottom:0;width:50%;background:#F4F3FF"></div>'
            f'<div class="kicker" style="position:absolute;left:64px;top:76px;font-size:20px">Trade-offs</div>'
            f'{_fig_title(title, False, 64, 112, 1400, 58)}'
            f'{card(64, left, False)}{card(64 + cw + 40, right, True)}'
            f'<div style="position:absolute;left:{64+cw+2}px;top:{ctop+chh//2-18}px;width:36px;height:36px;border-radius:50%;background:#fff;border:1px solid #DEDEE8;'
            f'display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:800;color:#5B5A7A;z-index:2">VS</div></div>')
    job(page(name, w, h, body), out, w, h)


# ---------------------------------------------------------------- v3: zoomed, readable UI crops
# crop boxes (source px) + callout points (source px) for each Drumee 2.0 screenshot
SHOT3 = {
    "files_chat": {"src": "ui2/files_chat.png", "box": (780, 110, 1389, 800),
                   "pts": [(960, 335, "File threads per document"), (1335, 552, "Live meeting card in chat"), (1345, 694, "Open the file's thread")]},
    "tasks": {"src": "ui2/tasks.png", "box": (290, 62, 1150, 700),
              "pts": [(850, 89, "Board, list, backlog, timeline, reports"), (842, 229, "Files linked to the card"), (738, 390, "Subtasks with status")]},
    "files": {"src": "ui2/files.png", "box": (285, 62, 1060, 560),
              "pts": [(390, 167, "Grouped by file type"), (545, 358, "Private files locked"), (680, 88, "Filter docs, PDF and media")]},
    "meeting": {"src": "ui2/meeting.png", "box": (740, 560, 1389, 860),
                "pts": [(1290, 640, "In-call chat beside the video"), (1290, 760, "Reactions and replies"), (1010, 800, "Share files in the call")]},
    "admin": {"src": "ui2/admin_manage.png", "box": (0, 0, 1026, 333),
              "pts": [(640, 58, "Members and roles"), (330, 193, "Approval requests"), (640, 193, "2-step verification")]},
}


def _crop_html(shot, w_px, rounded=18, markers=True, mark_offset=1):
    s = SHOT3[shot]; x0, y0, x1, y1 = s["box"]; cw, ch = x1 - x0, y1 - y0
    k = w_px / cw; h_px = round(ch * k)
    src = rel(os.path.join(HERE, s["src"]))
    img = (f'<div style="position:relative;width:{w_px}px;height:{h_px}px;border-radius:{rounded}px;overflow:hidden;'
           f'background:#fff;box-shadow:0 30px 70px -30px rgba(15,16,17,.55),0 0 0 1px rgba(15,16,17,.06)">'
           f'<img src="{src}" style="position:absolute;left:{-x0*k}px;top:{-y0*k}px;width:{Image_w(s["src"])*k}px">')
    if markers:
        for i, (px, py, _) in enumerate(s["pts"], mark_offset):
            img += (f'<div style="position:absolute;left:{(px-x0)*k-19}px;top:{(py-y0)*k-19}px;width:38px;height:38px;border-radius:50%;'
                    f'background:#433CC5;color:#fff;font-weight:800;font-size:19px;display:flex;align-items:center;justify-content:center;'
                    f'box-shadow:0 0 0 5px rgba(67,60,197,.22)">{i}</div>')
    return img + "</div>", h_px


def Image_w(path):
    from PIL import Image as _I
    return _I.open(os.path.join(HERE, path)).size[0]


def fig_product3(name, out, shot, title, scale=2):
    """Readable product figure: zoomed crop + numbered markers + legend."""
    w, h = 1600, 900
    s = SHOT3[shot]
    crop_w = 1000
    crop, ch = _crop_html(shot, crop_w)
    scale_fit = min(1, (h - 120) / ch)
    legend = "".join(f'<div style="display:flex;gap:16px;align-items:flex-start;margin-top:26px">'
                     f'<div style="flex:none;width:34px;height:34px;border-radius:50%;background:#fff;color:#433CC5;font-weight:800;font-size:17px;display:flex;align-items:center;justify-content:center">{i}</div>'
                     f'<div style="color:#fff;font-size:25px;font-weight:600;line-height:1.3;padding-top:2px">{esc(t)}</div></div>'
                     for i, (_, _, t) in enumerate(s["pts"], 1))
    body = (f'<div style="position:absolute;inset:0;background:#F4F3FF">'
            f'<div style="position:absolute;left:0;top:0;bottom:0;width:470px;background:#433CC5;overflow:hidden">{rings(0, 900, 300, 5)}</div>'
            f'<div style="position:absolute;left:56px;top:70px;width:370px">'
            f'<div style="color:rgba(255,255,255,.7);font-size:17px;font-weight:600;letter-spacing:.1em;text-transform:uppercase">Inside the product</div>'
            f'<div class="title" data-fit="370" style="color:#fff;font-size:44px;margin-top:18px;white-space:normal;line-height:1.08">{esc(title)}</div>'
            f'{legend}</div>'
            f'<div style="position:absolute;left:{470 + (1130 - crop_w*scale_fit)/2}px;top:{(h - ch*scale_fit)/2}px;transform:scale({scale_fit});transform-origin:0 0">{crop}</div></div>')
    job(page(name, w, h, body), out, w, h, scale)


def cover3(name, out, w, h, l1, l2, kicker, shot=None, variant="light", scale=2):
    """Clean editorial cover. variant 'light' = UI crop on purple panel; 'type' = typographic dark, no UI."""
    pad = round(h * 0.11)
    if variant == "type":
        fs = round(h * 0.15)
        body = (f'<div class="dark bgA" style="position:absolute;inset:0">{rings(w*0.86, h*0.5, h*0.5, 5, h*0.16)}'
                f'<div style="position:absolute;left:{pad}px;bottom:{pad}px;width:{round(w*0.78)}px">'
                f'<div class="kicker" style="font-size:{round(h*0.04)}px;margin-bottom:{round(h*0.05)}px">{esc(kicker)}</div>'
                f'<div class="title" data-fit="{round(w*0.78)}" style="font-size:{fs}px"><div class="l1">{esc(l1)}</div><div class="l2">{esc(l2)}</div></div></div></div>')
    else:
        panel_w = round(w * 0.46)
        crop_w = round(panel_w * 0.86)
        crop, ch = _crop_html(shot, crop_w, rounded=12, markers=False)
        fit = min(1, (h * 0.80) / ch)
        fs = round(h * 0.12)
        tw = round(w * 0.45)
        body = (f'<div class="light" style="position:absolute;inset:0;background:#fff">'
                f'<div style="position:absolute;right:0;top:0;bottom:0;width:{panel_w}px;background:#433CC5;overflow:hidden">{rings(panel_w, h, h*0.45, 5)}</div>'
                f'<div style="position:absolute;right:{round((panel_w-crop_w*fit)/2)}px;top:{round((h-ch*fit)/2)}px;transform:scale({fit});transform-origin:0 0">{crop}</div>'
                f'<div style="position:absolute;left:{pad}px;top:50%;transform:translateY(-50%);width:{tw}px">'
                f'<div class="kicker" style="font-size:{round(h*0.04)}px;margin-bottom:{round(h*0.05)}px">{esc(kicker)}</div>'
                f'<div class="title" data-fit="{tw}" style="font-size:{fs}px"><div class="l1">{esc(l1)}</div><div class="l2">{esc(l2)}</div></div></div></div>')
    job(page(name, w, h, body), out, w, h, scale)
