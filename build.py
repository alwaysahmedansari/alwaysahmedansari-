"""Generates the GitHub profile README + animated SVG cards (dark and light).
Edit the text/colours below, run `python3 build.py`, upload README.md and assets/ to your repo."""
import os, base64, shutil, xml.etree.ElementTree as ET
from string import Template

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT", HERE)
PFX = "" if os.environ.get("FLAT") else "assets/"
A = OUT + "/" + PFX.rstrip("/")
os.makedirs(A, exist_ok=True)

IG = "https://instagram.com/alwaysahmedansari"
TH_URL = "https://www.threads.net/@alwaysahmedansari"
HANDLE = "@alwaysahmedansari"

# One accent: a highlighter-yellow, the writer/researcher's tool. Ink-navy and paper-blue around it.
TH = {
    "light": dict(bg="#F4F7FB", border="#D9E1EC", ink="#0F2A43", sub="#34495E", muted="#5F7184",
                  hi="#FFD84D", hiop=".9", soft="#E8EEF6", line="#C5D0DE", green="#1F8A5B"),
    "dark": dict(bg="#0D1B2A", border="#22344A", ink="#EAF0F7", sub="#B9C6D6", muted="#8CA0B5",
                 hi="#FFD84D", hiop=".38", soft="#14283D", line="#2C415A", green="#4CC38A"),
}
SE = "Charter,'Bitstream Charter','Sitka Text',Cambria,Georgia,serif"
SA = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MO = "ui-monospace,Menlo,Consolas,monospace"
RM = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def tx(x, y, s, f, z, c, a="start", e=""):
    return f'<text x="{x}" y="{y}" font-family="{f}" font-size="{z}" fill="{c}" text-anchor="{a}" {e}>{s}</text>'


def svg(w, h, label, css, body, t, r=24):
    css = Template(css).substitute(t)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
            f'<title>{label}</title><style>{css}{RM}</style>'
            f'<rect width="{w}" height="{h}" rx="{r}" fill="{t["bg"]}"/>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{t["border"]}"/>{body}</svg>')


def pl(x1, y1, x2, c, sw, cls="", d=0, op=1):
    a = f' class="{cls}" pathLength="1" style="animation-delay:{d}s"' if cls else ""
    return f'<path d="M{x1} {y1}H{x2}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" fill="none" opacity="{op}"{a}/>'


def hi(x, y, w, h, t, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<rect{c} x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{t["hi"]}" opacity="{t["hiop"]}"/>'


PING = (".ping{animation:ping 2s ease-out infinite;transform-origin:center;transform-box:fill-box}"
        "@keyframes ping{0%{transform:scale(1);opacity:.5}100%{transform:scale(3);opacity:0}}")


def header(t):
    css = (".hl{transform-origin:left;transform-box:fill-box;animation:hl 8s ease-out infinite}"
           "@keyframes hl{0%{transform:scaleX(0);opacity:1}25%,82%{transform:scaleX(1);opacity:1}100%{transform:scaleX(1);opacity:0}}" + PING)
    p = f'<g transform="translate(830 62) rotate(2.5)"><rect width="290" height="320" rx="16" fill="{t["soft"]}" stroke="{t["line"]}"/>'
    p += hi(24, 148, 214, 16, t) + hi(24, 238, 124, 16, t) + pl(30, 54, 150, t["ink"], 9)
    for i, wd in enumerate([230, 200, 236, 170, 226, 120, 210]):
        p += pl(30, 96 + i * 30, 30 + wd, t["muted"], 5, op=.55)
    p += "</g>"
    b = p + tx(60, 96, "Freelance writer and researcher", SA, 20, t["muted"])
    b += hi(58, 172, 560, 40, t, "hl")
    b += tx(58, 206, "Ahmed Ansari", SE, 92, t["ink"], e='font-weight="700" textLength="560" lengthAdjust="spacingAndGlyphs"')
    b += tx(60, 262, "Words, research, and the occasional build.", SE, 30, t["sub"], e='font-style="italic"')
    b += tx(60, 302, "Based in Lahore, Pakistan.", SA, 19, t["muted"])
    b += (f'<rect x="60.5" y="344.5" width="300" height="44" rx="22" fill="none" stroke="{t["line"]}"/>'
          f'<circle class="ping" cx="86" cy="366" r="5" fill="{t["green"]}"/><circle cx="86" cy="366" r="5" fill="{t["green"]}"/>'
          + tx(106, 371, "Open for freelance work", SA, 16, t["ink"]))
    return svg(1200, 440, "Ahmed Ansari, freelance writer and researcher in Lahore, Pakistan. Open for freelance work.", css, b, t, 28)


def write_css(d):
    return (f".w{{stroke-dasharray:1;animation:write {d}s ease-in-out infinite both}}"
            "@keyframes write{0%{stroke-dashoffset:1;opacity:0}2%{opacity:1}10%,88%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:1;opacity:0}}")


BLINK = ".cur{animation:blink 1.1s steps(1) infinite}@keyframes blink{0%,49%{fill:$hi}50%,100%{fill:transparent}}"


def icon(kind, t):
    pap = f'<rect x="430" y="62" width="100" height="126" rx="10" fill="{t["soft"]}" stroke="{t["line"]}"/>'
    if kind == "write":
        b = pap + pl(448, 88, 486, t["ink"], 6, "w", 0)
        for i, x2 in enumerate([512, 500, 512, 486]):
            b += pl(448, 110 + i * 16, x2, t["muted"], 5, "w", round(.6 * (i + 1), 1), .7)
        return write_css(7), b
    if kind == "lens":
        b = pap + pl(448, 88, 486, t["ink"], 6) + hi(444, 119, 62, 14, t)
        for i, x2 in enumerate([512, 500, 512, 486]):
            b += pl(448, 110 + i * 16, x2, t["muted"], 5, op=.55)
        b += (f'<g transform="translate(468 118)"><g class="lens"><circle r="22" fill="{t["hi"]}" fill-opacity=".12" stroke="{t["ink"]}" stroke-width="5"/>'
              f'<path d="M16 16L34 34" stroke="{t["ink"]}" stroke-width="7" stroke-linecap="round"/></g></g>')
        return (".lens{animation:dr 9s ease-in-out infinite}"
                "@keyframes dr{0%,100%{transform:translate(0,0)}33%{transform:translate(14px,8px)}66%{transform:translate(-4px,26px)}}"), b
    if kind == "ghost":
        g = ('<path d="M0 44V18C0 8 9 0 20 0S40 8 40 18V44L33.3 38 26.7 44 20 38 13.3 44 6.7 38Z" '
             f'fill="{t["soft"]}" stroke="{t["ink"]}" stroke-width="1.4"/><circle cx="14" cy="19" r="2.6" fill="{t["ink"]}"/><circle cx="26" cy="19" r="2.6" fill="{t["ink"]}"/>')
        b = (f'<ellipse class="sh" cx="480" cy="170" rx="30" ry="5" fill="{t["line"]}"/>'
             f'<g transform="translate(442 66)"><g class="fl"><g transform="scale(1.9)">{g}</g></g></g>')
        return (".fl{animation:fl 3.4s ease-in-out infinite}@keyframes fl{0%,100%{transform:translate(0,0)}50%{transform:translate(0,-10px)}}"
                ".sh{animation:sh 3.4s ease-in-out infinite;transform-origin:center;transform-box:fill-box}"
                "@keyframes sh{0%,100%{transform:scale(1)}50%{transform:scale(.75)}}"), b
    b = (f'<rect x="428" y="64" width="108" height="112" rx="12" fill="{t["soft"]}" stroke="{t["line"]}"/>'
         + "".join(f'<circle cx="{x}" cy="80" r="4" fill="{t["line"]}"/>' for x in (444, 458, 472))
         + f'<path d="M428 94H536" stroke="{t["line"]}"/>'
         + tx(482, 146, f'&lt;/&gt;<tspan class="cur" fill="{t["hi"]}">_</tspan>', MO, 36, t["ink"], "middle", 'font-weight="700"'))
    return BLINK, b


SV = [("write", "Article Writing", "Clear, well-researched articles", "for your blog, site or brand."),
      ("lens", "Research", "Deep dives, source checking, and", "findings you can actually use."),
      ("ghost", "Ghostwriting", "I write it. You publish it", "under your own name."),
      ("code", "Coding &amp; Builds", "Mid-level builds when a project", "needs code. Honest about my limits.")]


def service(kind, title, l1, l2, t):
    css, ic = icon(kind, t)
    b = (tx(32, 86, title, SE, 42, t["ink"], e='font-weight="700"')
         + f'<rect x="32" y="102" width="56" height="8" rx="4" fill="{t["hi"]}"/>'
         + tx(32, 146, l1, SA, 17, t["sub"]) + tx(32, 172, l2, SA, 17, t["sub"])
         + f'<g transform="translate(0 -14)">{ic}</g>')
    return svg(580, 220, f"{title}: {l1} {l2}", css, b, t)


def social(kind, t):
    name = "Instagram" if kind == "ig" else "Threads"
    if kind == "ig":
        g = (f'<rect x="47" y="47" width="26" height="26" rx="8" fill="none" stroke="{t["ink"]}" stroke-width="2.2"/>'
             f'<circle cx="60" cy="60" r="6" fill="none" stroke="{t["ink"]}" stroke-width="2.2"/><circle cx="67" cy="53" r="1.6" fill="{t["ink"]}"/>')
    else:
        g = tx(60, 71, "@", SE, 30, t["ink"], "middle", 'font-weight="700"')
    b = (f'<circle cx="60" cy="60" r="30" fill="{t["soft"]}" stroke="{t["line"]}"/>' + g
         + tx(112, 42, name, SA, 15, t["muted"]) + tx(112, 80, HANDLE, SE, 30, t["ink"], e='font-weight="700"')
         + tx(112, 102, "Say hello or follow along.", SA, 14, t["muted"])
         + tx(536, 76, "↗", SA, 28, t["ink"], "middle")
         + f'<rect x="112" y="86" width="0" height="0"/>')
    return svg(580, 120, f"Ahmed Ansari on {name}, {HANDLE}", "", b, t)


for th, t in TH.items():
    def w(n, s):
        open(f"{A}/{n}-{th}.svg", "w", encoding="utf-8").write(s)
    w("header", header(t))
    for i, s in enumerate(SV, 1):
        w(f"svc{i}", service(*s, t))
    w("ig", social("ig", t))
    w("th", social("th", t))
for f in [x for x in os.listdir(A) if x.endswith(".svg")]:
    ET.parse(f"{A}/{f}")  # fails loudly if any SVG is not well-formed XML


def pic(n, alt, wd="", m="file"):
    def s(th):
        if m == "file":
            return f"{PFX}{n}-{th}.svg"
        return "data:image/svg+xml;base64," + base64.b64encode(open(f"{A}/{n}-{th}.svg", "rb").read()).decode()
    wa = f' width="{wd}"' if wd else ""
    return f'<picture><source media="(prefers-color-scheme: dark)" srcset="{s("dark")}"><img src="{s("light")}" alt="{alt}"{wa}></picture>'


def doc(m):
    p = lambda *a: pic(*a, m=m)
    cards = [p(f"svc{i}", f"{s[1].replace('&amp;', 'and')}: {s[2]} {s[3]}", "49%") for i, s in enumerate(SV, 1)]
    return f'''<div align="center">
{p("header", "Ahmed Ansari, freelance writer and researcher in Lahore, Pakistan. Open for freelance work.")}
</div>

<p>I write, research and ghostwrite: articles, deep dives, and words that go out under your name. I also code a little. I’m not a software engineer, but I can build mid-level things, and I’ll tell you plainly which jobs fit.</p>

<h2>What I do</h2>

<p>
  {cards[0]}
  {cards[1]}
</p>
<p>
  {cards[2]}
  {cards[3]}
</p>

<h2>Find me</h2>

<p>
  <a href="{IG}">{p("ig", f"Ahmed Ansari on Instagram, {HANDLE}", "49%")}</a>
  <a href="{TH_URL}">{p("th", f"Ahmed Ansari on Threads, {HANDLE}", "49%")}</a>
</p>

<p align="center"><sub>Open to freelance writing, research and ghostwriting projects.</sub></p>
<!-- add email / portfolio links here later -->
'''


open(OUT + "/README.md", "w", encoding="utf-8").write(doc("file"))

if os.environ.get("PREVIEW"):
    css = ("""<style>:root{--bg:#fff;--fg:#1f2328;--mu:#59636e;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0d1117;--fg:#e6edf3;--mu:#9198a1}}
:root[data-theme="dark"]{--bg:#0d1117;--fg:#e6edf3;--mu:#9198a1}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,'Segoe UI',Helvetica,Arial,sans-serif}
main{max-width:860px;margin:0 auto;padding:20px 16px 40px}
h2{margin:28px 0 12px;padding-bottom:6px;border-bottom:1px solid rgba(128,128,128,.3);font-size:24px}
p{margin:0 0 12px}img{max-width:100%;height:auto;vertical-align:top}
div[align=center] img{width:100%}.note{color:var(--mu);font-size:13px;margin-top:28px}</style>""")
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'<title>Ahmed Ansari: profile preview</title>{css}</head><body><main>{doc("data")}'
            '<p class="note">Preview of the GitHub profile README. Email and portfolio links can be added later.</p></main></body></html>')
    open(os.environ["PREVIEW"], "w", encoding="utf-8").write(html)
