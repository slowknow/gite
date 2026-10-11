#!/usr/bin/env python3
"""Build the static site: site/index.html (nl), site/<lang>/index.html, site/style.css, site/img/.

Content lives in content/<lang>.py, structure in page.html, the document skeleton in template.html.
`python3 build.py` writes site/; `python3 build.py --artifact` also writes artifact/index.html,
the Dutch page without the document skeleton, for publishing as a claude.ai artifact.
"""
import importlib.util, shutil, sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
LANGS = ["nl", "fr", "en", "de"]
LANG_NAMES = {"nl": "NL", "fr": "FR", "en": "EN", "de": "DE"}
SITE_URL = "https://poirier.ceder.dev/"  # for hreflang links; the real domain once it moves from Wix


def load(lang):
    spec = importlib.util.spec_from_file_location(lang, ROOT / "content" / f"{lang}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def floors(items):
    out = []
    for name, lines in items:
        lis = "".join(f"<li>{escape(l)}</li>" for l in lines)
        out.append(f'<div class="floor"><p class="eyebrow">{escape(name)}</p><ul>{lis}</ul></div>')
    return "\n".join(out)


def render(c, prefix):
    lang_links = " ".join(
        f'<a href="{prefix}{"" if l == "nl" else l + "/"}index.html" lang="{l}" hreflang="{l}"'
        + (' aria-current="page"' if l == c.lang else "") + f">{LANG_NAMES[l]}</a>"
        for l in LANGS
    )
    v = {
        "p": prefix,
        "lang_links": lang_links,
        "hero_facts": "".join(f"<span>{escape(f)}</span>" for f in c.hero_facts),
        "intro_paragraphs": "\n".join(f"<p>{p}</p>" for p in c.intro_paragraphs),
        "facts": "".join(f'<div class="troef"><b>{escape(b)}</b><small>{escape(s)}</small></div>' for b, s in c.facts),
        "woonhuis_floors": floors(c.woonhuis_floors),
        "schuur_floors": floors(c.schuur_floors),
        "gallery": "".join(
            f'<figure class="photo"><img src="{prefix}img/{img}.jpg" alt="{escape(cap)}" loading="lazy"><figcaption>{escape(cap)}</figcaption></figure>'
            for img, cap in c.gallery),
        "garden_chips": "".join(f"<li>{escape(x)}</li>" for x in c.garden_chips),
        "area_cards": "".join(
            f'<div class="card"><h3>{escape(h)}</h3><ul>'
            + "".join(f"<li><span>{escape(a)}</span><span>{escape(b)}</span></li>" for a, b in items)
            + "</ul></div>" for h, items in c.area_cards),
        "directions": "".join(f"<details><summary>{escape(s)}</summary><p>{escape(t)}</p></details>" for s, t in c.directions),
    }
    for k in dir(c):
        if not k.startswith("_") and k not in v:
            val = getattr(c, k)
            if isinstance(val, str):
                v[k] = val
    page = (ROOT / "page.html").read_text()
    return page.format(**v), v


def main():
    site = ROOT / "site"
    site.mkdir(exist_ok=True)
    shutil.copy(ROOT / "style.css", site / "style.css")
    shutil.copy(ROOT / "robots.txt", site / "robots.txt")  # preview: blocks every crawler
    if (site / "img").exists():
        shutil.rmtree(site / "img")
    shutil.copytree(ROOT / "img", site / "img", ignore=shutil.ignore_patterns("raw"))
    template = (ROOT / "template.html").read_text()
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE_URL}{"" if l == "nl" else l + "/"}">' for l in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE_URL}">'
    for lang in LANGS:
        c = load(lang)
        prefix = "" if lang == "nl" else "../"
        page, v = render(c, prefix)
        doc = template.format(lang=lang, title=c.title, meta_description=escape(c.meta_description),
                              alternates=alternates, p=prefix, page=page)
        out = site / ("index.html" if lang == "nl" else f"{lang}/index.html")
        out.parent.mkdir(exist_ok=True)
        out.write_text(doc)
        print("wrote", out.relative_to(ROOT))
    if "--artifact" in sys.argv:
        c = load("nl")
        page, _ = render(c, "")
        head = (f"<title>{c.title}</title>\n"
                '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Nunito+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap">\n'
                '<link rel="stylesheet" href="style.css">\n')
        art = ROOT / "artifact"
        art.mkdir(exist_ok=True)
        (art / "index.html").write_text(head + page)
        print("wrote artifact/index.html")


if __name__ == "__main__":
    main()
