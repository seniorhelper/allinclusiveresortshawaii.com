# Static site builder for allinclusiveresortshawaii.com
# Run: python _build/build.py   (writes pages into the repo root)
# Keeps header/footer/schema consistent. Content lives in _build/pages.py.
import json, os, html
from pages import PAGES, SITE, UPDATED, UPDATED_HUMAN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = SITE["url"]

NAV = [
    ("/", "Home"),
    ("/ways-to-go-all-inclusive-in-hawaii/", "Ways to do it"),
    ("/islands/", "By island"),
    ("/cost/", "Cost"),
    ("/whats-included/", "What's included"),
    ("/families-and-couples/", "Families & couples"),
]

CSP = ("default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; "
       "font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'")

LOGO_SVG = ('<svg width="40" height="40" viewBox="0 0 40 40" aria-hidden="true" focusable="false">'
            '<circle cx="20" cy="20" r="19" fill="#088395"/><circle cx="27" cy="14" r="6" fill="#f2a541"/>'
            '<path d="M3 25c5-4 9-4 14 0s9 4 14 0 6-3 6-3v8a19 19 0 0 1-34 0z" fill="#fdf8f0"/></svg>')

WAVES = ('<svg class="waves" viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
         '<path d="M0 38c120-22 240-22 360 0s240 22 360 0 240-22 360 0 240 22 360 0v32H0z" fill="#fffdf9"/></svg>')


def org():
    return {"@type": "Organization", "@id": BASE + "/#org", "name": SITE["name"], "url": BASE + "/",
            "logo": BASE + "/assets/logo.png"}


def head(p):
    url = BASE + p["path"]
    title = html.escape(p["title"])
    desc = html.escape(p["description"])
    out = [
        '<!DOCTYPE html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<meta http-equiv="Content-Security-Policy" content="{CSP}">',
        '<meta name="referrer" content="strict-origin-when-cross-origin">',
        f'<title>{title}</title>',
        f'<meta name="description" content="{desc}">',
        ('<meta name="robots" content="noindex">' if p.get("noindex") else f'<link rel="canonical" href="{url}">\n<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">'),
        '<meta name="theme-color" content="#053b52">',
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '<link rel="stylesheet" href="/assets/site.css">',
        '<meta property="og:type" content="article">' if p["path"] != "/" else '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{SITE["name"]}">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{BASE}/assets/og.jpg">',
        '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
        '<meta property="og:locale" content="en_US">',
        '<meta name="twitter:card" content="summary_large_image">',
    ]
    for block in ([] if p.get("noindex") else schema(p)):
        out.append('<script type="application/ld+json">' + json.dumps(block, ensure_ascii=False, separators=(",", ":")) + '</script>')
    out.append('</head>')
    return "\n".join(out)


def schema(p):
    url = BASE + p["path"]
    blocks = []
    graph = []
    if p["path"] == "/":
        graph.append(org())
        graph.append({"@type": "WebSite", "@id": BASE + "/#site", "name": SITE["name"], "url": BASE + "/",
                      "publisher": {"@id": BASE + "/#org"}, "inLanguage": "en-US"})
    art_type = p.get("schema_type", "Article")
    if art_type:
        a = {"@type": art_type, "headline": p["h1"], "description": p["description"], "url": url,
             "mainEntityOfPage": url, "datePublished": p.get("published", UPDATED), "dateModified": UPDATED,
             "inLanguage": "en-US", "author": {"@type": "Organization", "name": SITE["name"], "url": BASE + "/about/"},
             "publisher": org(), "image": BASE + "/assets/og.jpg"}
        if p.get("about_place", True):
            a["about"] = {"@type": "Place", "name": "Hawaii, United States"}
        graph.append(a)
    if p["path"] != "/":
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}]
        items.append({"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url})
        graph.append({"@type": "BreadcrumbList", "itemListElement": items})
    if p.get("faq"):
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in p["faq"]]})
    blocks.append({"@context": "https://schema.org", "@graph": graph})
    return blocks


def strip_tags(s):
    import re
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def header(p):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == p["path"] else ""
        items.append(f'<li><a href="{href}"{cur}>{html.escape(label)}</a></li>')
    return (
        '<body>\n<a class="skip" href="#main">Skip to content</a>\n'
        '<header class="site-head"><div class="wrap">'
        f'<a class="brand" href="/">{LOGO_SVG}<span>{SITE["name"]}<small>The honest guide to all-inclusive-style Hawaii</small></span></a>'
        '<nav aria-label="Main"><ul class="nav">' + "".join(items) + '</ul></nav>'
        '</div></header>'
    )


def page_head(p):
    if p["path"] == "/":
        return (f'<section class="hero"><div class="wrap"><h1>{p["h1"]}</h1>'
                f'<p class="lede">{p["lede"]}</p>'
                '<div class="btns"><a class="btn btn-sun" href="/ways-to-go-all-inclusive-in-hawaii/">See the 6 ways to get close</a>'
                '<a class="btn btn-ghost" href="/cost/">Estimate your trip cost</a></div>'
                f'<p class="meta">Updated <time datetime="{UPDATED}">{UPDATED_HUMAN}</time> · Independent guide, no paid placements</p>'
                f'</div>{WAVES}</section>')
    return ('<div class="page-head"><div class="wrap">'
            '<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>'
            f'<li aria-current="page">{html.escape(p["crumb"])}</li></ol></nav>'
            f'<h1>{p["h1"]}</h1><p class="lede">{p["lede"]}</p>'
            f'<p class="meta">Updated <time datetime="{UPDATED}">{UPDATED_HUMAN}</time></p>'
            '</div></div>')


def faq_html(p):
    if not p.get("faq"):
        return ""
    rows = "".join(f'<details><summary>{html.escape(q)}</summary><div class="a"><p>{a}</p></div></details>'
                   for q, a in p["faq"])
    title = p.get("faq_title", "Frequently asked questions")
    return (f'<section class="section alt" aria-labelledby="faq"><div class="wrap narrow faq">'
            f'<h2 id="faq">{title}</h2>{rows}</div></section>')


def footer():
    links = "".join(f'<li><a href="{h}">{html.escape(l)}</a></li>' for h, l in NAV[1:])
    return (
        '<footer class="site-foot"><div class="wrap"><div class="foot-grid">'
        f'<div><h2>{SITE["name"]}</h2><p>An independent, plain-English guide to getting an all-inclusive-style vacation in Hawaii, '
        'written for travelers, not advertisers.</p></div>'
        f'<div><h2>Guides</h2><ul>{links}</ul></div>'
        '<div><h2>About this site</h2><ul><li><a href="/about/">About &amp; how we research</a></li>'
        '<li><a href="/privacy/">Privacy</a></li><li><a href="/image-credits/">Image credits</a></li>'
        '<li><a href="/sitemap.xml">Sitemap</a></li></ul></div>'
        '</div><p class="fine">Not affiliated with any resort, cruise line, airline or the State of Hawaii. '
        'Rates, fees, taxes and policies change often; confirm everything with the provider before you book. '
        '© 2026 All Inclusive Resorts Hawaii. Site by <a href="https://www.eyetoad.com/" rel="nofollow">Eye To Ad Media</a>.</p>'
        '</div></footer>'
    )


def render(p):
    scripts = "".join(f'<script src="{s}" defer></script>' for s in p.get("scripts", []))
    body = (header(p) + '\n<main id="main">' + page_head(p) + p["body"] + faq_html(p) + '</main>\n'
            + footer() + scripts + '\n</body>\n</html>\n')
    return head(p) + "\n" + body


def main():
    for p in PAGES:
        rel = p["path"].strip("/")
        out = os.path.join(ROOT, rel, "index.html") if rel and not rel.endswith(".html") else os.path.join(ROOT, rel or "index.html")
        if rel == "":
            out = os.path.join(ROOT, "index.html")
        if p.get("file"):
            out = os.path.join(ROOT, p["file"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(render(p))
        print("wrote", os.path.relpath(out, ROOT))
    # sitemap
    urls = "".join(f"<url><loc>{BASE}{p['path']}</loc><lastmod>{UPDATED}</lastmod></url>"
                   for p in PAGES if not p.get("noindex"))
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                + urls + "</urlset>\n")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
