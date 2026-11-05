#!/usr/bin/env python3
"""Build the Quincy Lou site.

Reads content/site.json and writes static HTML into site/.
Run from the repo root:   python3 tools/build.py

Only standard-library Python is used, so there is nothing to install.
The generated HTML is committed, so Netlify needs no build step.
"""
from __future__ import annotations

import html
import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
C = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))
S = C["site"]

FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800"
         "&family=Geist:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap")


def e(text: str) -> str:
    """Escape text for HTML."""
    return html.escape(str(text), quote=True)


# --------------------------------------------------------------------- icons
def icon(name: str, cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    paths = {
        "arrow": '<path d="M4 12 12 4M5.5 4H12v6.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        "back": '<path d="M13 8H3m4.5-4.5L3 8l4.5 4.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        "check": '<path d="m3 8.5 3.2 3L13 4.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        "play": '<path d="M4 2.5v11l9-5.5z" fill="#fff"/>',
        "spark": '<path d="M8 1.5c.4 3.3 2.2 5.1 5.5 5.5-3.3.4-5.1 2.2-5.5 5.5-.4-3.3-2.2-5.1-5.5-5.5C5.8 6.6 7.6 4.8 8 1.5Z" fill="currentColor"/>',
        "asterisk": '<path d="M8 2v12M2.8 5l10.4 6M2.8 11l10.4-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "star4": '<path d="M8 2v12M2 8h12M3.8 3.8l8.4 8.4M12.2 3.8l-8.4 8.4" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>',
        "pen": '<path d="M4 20 5.5 14 15 4.5l4.5 4.5L10 18.5zM13 6.5 17.5 11" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
        "cursor": '<path d="m5 4 13 5.5-5.6 1.9-1.9 5.6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M3 15.5l2-1M15 20l-.6-2.2M20 13.5l-2.1-.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
        "chart": '<path d="M4 20V10m6 10V4m6 16v-7m4 7H2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
        "search": '<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m15.5 15.5 5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
        "next": '<path d="M5 24h38M30 11l13 13-13 13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
        "quote": '<path d="M0 40V24C0 10 7 2 20 0l2 6c-7 2-11 7-11 14h9v20zm30 0V24C30 10 37 2 50 0l2 6c-7 2-11 7-11 14h9v20z" fill="currentColor"/>',
        "star": '<path d="m12 2.6 2.9 6 6.5.8-4.8 4.5 1.2 6.5L12 17.3l-5.8 3.1 1.2-6.5-4.8-4.5 6.5-.8z" fill="currentColor"/>',
        "right": '<path d="M5 12h14m-6-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        "left": '<path d="M19 12H5m6-6-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        "phone": '<path d="M6.6 3.5h2.8l1.4 4.2-2 1.4a12 12 0 0 0 6.1 6.1l1.4-2 4.2 1.4v2.8a2 2 0 0 1-2.2 2A17 17 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
        "mark": '<path d="M12 1.5 22.5 12 12 22.5 1.5 12z" fill="currentColor"/><path d="M12 7.5 16.5 12 12 16.5 7.5 12z" style="fill: var(--mark-hole, #1487D2)"/>',
        "linkedin": '<path d="M5 9h3v10H5zM6.5 4.5a1.75 1.75 0 1 1 0 3.5 1.75 1.75 0 0 1 0-3.5ZM10.5 9h2.9v1.4c.4-.8 1.5-1.6 3.1-1.6 3.2 0 3.8 2 3.8 4.7V19h-3v-4.9c0-1.2 0-2.6-1.6-2.6s-1.9 1.2-1.9 2.5v5h-3.3z" fill="currentColor"/>',
        "instagram": '<rect x="3.5" y="3.5" width="17" height="17" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.2" cy="6.8" r="1.2" fill="currentColor"/>',
        "dribbble": '<circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M5 7.5c4 3.5 9 4.8 14.5 3.6M8.5 4.5c3 4 5 9 5.5 15M4 14.5c4-2.5 9-3 14 0" fill="none" stroke="currentColor" stroke-width="1.6"/>',
    }
    vb = {"pen": "0 0 24 24", "cursor": "0 0 24 24", "chart": "0 0 24 24", "search": "0 0 24 24",
          "next": "0 0 48 48", "quote": "0 0 52 40", "star": "0 0 24 24", "right": "0 0 24 24",
          "left": "0 0 24 24", "phone": "0 0 24 24", "mark": "0 0 24 24", "linkedin": "0 0 24 24",
          "instagram": "0 0 24 24", "dribbble": "0 0 24 24"}.get(name, "0 0 16 16")
    return f'<svg{c} viewBox="{vb}" aria-hidden="true">{paths[name]}</svg>'


def btn(label: str, href: str, kind: str = "cta", size: str = "", arrow: bool = True, extra: str = "") -> str:
    cls = f"btn btn--{kind}" + (f" btn--{size}" if size else "") + (f" {extra}" if extra else "")
    a = icon("arrow", "arr") if arrow else ""
    return f'<a class="{cls}" href="{e(href)}">{e(label)}{a}</a>'


def acc_title(parts: list[str], tag: str = "h2", attrs: str = "", one_line: bool = False) -> str:
    """Two-part headline: the first part in the grotesk, the second as the italic accent."""
    first, second = parts
    gap = " " if one_line else "<br>"
    return f'<{tag}{attrs}>{e(first)}{gap}<span class="acc">{e(second)}</span></{tag}>'


def ph(label: str, cls: str = "ph--r43", extra: str = "") -> str:
    """A blank image placeholder that still tells a screen reader what belongs there."""
    return f'<span class="ph {cls}{" " + extra if extra else ""}" role="img" aria-label="{e(label)}"></span>'


def nice_date(iso: str) -> str:
    d = date.fromisoformat(iso)
    return d.strftime("%-d %b %Y")


# ------------------------------------------------------------- page chrome
NAV = [("Work", "/work/"), ("Services", "/#services"), ("Pricing", "/#pricing"),
       ("Studio", "/studio/"), ("Journal", "/journal/")]


def head(title: str, desc: str, path: str) -> str:
    full = title if title == S["name"] else f"{title} | {S['name']}"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(S['url'] + path)}">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{e(S['url'] + path)}">
<meta name="theme-color" content="#FDF9F1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%23F46840'/%3E%3Cpath d='M16 8v16M8 16h16M10.3 10.3l11.4 11.4M21.7 10.3 10.3 21.7' stroke='%23000' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active: str = "") -> str:
    current = ' aria-current="page"'
    links = "".join(
        f'<a href="{href}"{current if label == active else ""}>{label}</a>'
        for label, href in NAV)
    mlinks = "".join(f'<a href="{href}">{label}</a>' for label, href in NAV)
    return f"""<header class="hdr">
  <div class="wrap hdr__in">
    <a class="logo" href="/" aria-label="{e(S['name'])}, home">{e(S['name'])}<i aria-hidden="true"></i></a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <div class="hdr__right">
      <a class="hdr__phone" href="tel:{S['phone_href']}">{e(S['phone'])}</a>
      {btn(S['cta'], '/contact/', 'cta')}
      <details class="menu">
        <summary>Menu</summary>
        <nav class="menu__panel" aria-label="Mobile">{mlinks}<a href="/contact/">Contact</a>
          <a class="btn btn--cta" href="tel:{S['phone_href']}">Call {e(S['phone'])}</a>
        </nav>
      </details>
    </div>
  </div>
</header>
"""


def enquiry_form(form_id: str = "review") -> str:
    ct = C["contact"]
    needs = "".join(
        f'<label class="chip"><input type="checkbox" name="need" value="{e(n)}"><span>{e(n)}</span></label>'
        for n in ct["needs"])
    budgets = "".join(
        f'<label class="chip"><input type="radio" name="budget" value="{e(b)}"><span>{e(b)}</span></label>'
        for b in ct["budgets"])
    return f"""<form class="form" name="{form_id}" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="company-website">
  <input type="hidden" name="form-name" value="{form_id}">
  <p class="hp"><label>Leave this empty <input name="company-website" tabindex="-1" autocomplete="off"></label></p>
  <fieldset><legend>What do you need?</legend><div class="chips">{needs}</div></fieldset>
  <fieldset><legend>Rough budget</legend><div class="chips">{budgets}</div></fieldset>
  <fieldset><legend>Who are you?</legend>
    <div class="fields">
      <label><span class="sr-only">Your name</span><input class="input" name="name" placeholder="Your name" autocomplete="name" required></label>
      <label><span class="sr-only">Email</span><input class="input" type="email" name="email" placeholder="Email" autocomplete="email" required></label>
    </div>
    <label><span class="sr-only">Website address</span><input class="input" name="website" placeholder="Your current website (if you have one)" inputmode="url"></label>
  </fieldset>
  <label><span class="lbl" style="display:block">What isn’t working?</span>
    <textarea class="input" name="message" placeholder="What does the business do, and what would a good month of enquiries look like?"></textarea></label>
  <button class="btn btn--cta btn--block" type="submit">Send and get my review{icon('arrow', 'arr')}</button>
  <p class="form__fine">{e(S['reply_time'])}. No newsletter unless you ask for it.</p>
</form>"""


def footer() -> str:
    nav = "".join(f'<li><a href="{href}">{label}</a></li>' for label, href in NAV)
    social = "".join(f'<li><a href="{e(s["href"])}">{e(s["label"])}</a></li>' for s in S["social"])
    addr = "".join(f"<li>{e(line)}</li>" for line in S["address"])
    return f"""<div class="ftr-wrap">
<footer class="ftr">
  <div class="ftr__cta">
    <h2>Got a website that<br><span class="acc">should do more?</span></h2>
    <div class="ftr__contact">
      {btn('Get a free website review', '/contact/', 'cta')}
      <a class="ftr__mail" href="mailto:{e(S['email'])}">{e(S['email'])}</a>
      <a href="tel:{S['phone_href']}">{e(S['phone'])}</a>
    </div>
  </div>
  <div class="ftr__cols">
    <div><h3>Studio</h3><ul>{addr}<li>{e(S['hours'])}</li></ul></div>
    <div><h3>Pages</h3><ul>{nav}<li><a href="/contact/">Contact</a></li></ul></div>
    <div><h3>Elsewhere</h3><ul>{social}</ul></div>
    <div class="ftr__news"><h3>Field notes</h3>
      <p>One email a month on what is making websites bring in more work. Unsubscribe any time.</p>
      <form name="newsletter" method="POST" action="/thanks/" data-netlify="true">
        <input type="hidden" name="form-name" value="newsletter">
        <label class="sr-only" for="nl-email">Email</label>
        <input class="input" id="nl-email" type="email" name="email" placeholder="you@company.com" required>
        <button class="btn btn--cta" type="submit">Join</button>
      </form>
    </div>
  </div>
  <span class="wordmark" aria-hidden="true">{e(S['name'])}</span>
  <div class="ftr__base">
    <span>© {date.today().year} {e(S['company'])}</span>
    <nav aria-label="Legal"><a href="/privacy/">Privacy</a><a href="/contact/">Contact</a></nav>
  </div>
</footer>
</div>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def page(path: str, title: str, desc: str, body: str, active: str = "") -> None:
    out = SITE / path.strip("/") / "index.html" if path != "/404" else SITE / "404.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head(title, desc, path) + header(active) + f'<main id="main">\n{body}\n</main>\n' + footer(),
                   encoding="utf-8")


# ---------------------------------------------------------------- components
def work_card(w: dict, ratio: str) -> str:
    return f"""<a class="card-work" href="/work/{e(w['slug'])}/" data-r>
  <div class="card-work__media">
    <span class="badge">{icon('arrow')}{e(w['result'])}</span>
    {ph(f"{w['name']} project image", ratio)}
  </div>
  <div class="card-work__row">
    <div><h3>{e(w['name'])}</h3><p class="card-work__line">{e(w['line'])}</p></div>
    <div class="tags"><span class="tag">{e(w['service'])}</span><span class="tag tag--fill">{e(w['year'])}</span></div>
  </div>
</a>"""


def work_grid(items: list[dict]) -> str:
    """Two staggered columns that start and end level.

    The left column runs tall, short, tall, short; the right runs short, tall,
    short, tall. Both start at the same top and, with equal counts, add up to
    the same height, so the stagger is in the middle and the edges line up.
    """
    a = [w for i, w in enumerate(items) if i % 2 == 0]
    b = [w for i, w in enumerate(items) if i % 2 == 1]
    col_a = "".join(work_card(w, "ph--r45" if i % 2 == 0 else "ph--r43") for i, w in enumerate(a))
    col_b = "".join(work_card(w, "ph--r43" if i % 2 == 0 else "ph--r45") for i, w in enumerate(b))
    return f'<div class="work-grid"><div class="work-col">{col_a}</div><div class="work-col">{col_b}</div></div>'


def post_card(p: dict, idx: int = 0) -> str:
    return f"""<a class="post" href="/journal/{e(p['slug'])}/" data-r="{idx * 80}">
  {ph(f"Cover image for {p['title']}", "ph--r43")}
  <div class="post__meta"><span class="chip-ink">{e(p['tag'])}</span><span>{nice_date(p['date'])}</span></div>
  <h3>{e(p['title'])}</h3>
</a>"""


def team_block() -> str:
    cards = "".join(f"""<div class="member" data-r="{i * 70}">
  {ph(f"Portrait of {m['name']}", "ph--r45")}
  <h3>{e(m['name'])}</h3><p class="member__role">{e(m['role'])}</p><p class="member__line">{e(m['line'])}</p>
</div>""" for i, m in enumerate(C["team"]))
    return f'<div class="team">{cards}</div>'


def enquire_block(form_id: str = "review", tag: str = "h2", cls: str = "band") -> str:
    h = C["home"]
    return f"""<section class="{cls}" id="enquire" aria-labelledby="enq-h">
  <div class="wrap">
    <div class="enquire" data-r>
      <div>
        {acc_title(h['form_title'], tag, ' id="enq-h"')}
        <p class="enquire__lede">{e(h['form_lede'])}</p>
        <div class="enquire__alt">
          <a href="mailto:{e(S['email'])}">Prefer email? {e(S['email'])}</a>
          <a href="tel:{S['phone_href']}">Or ring {e(S['phone'])}</a>
          <span>{e(S['reply_time'])}.</span>
        </div>
      </div>
      {enquiry_form(form_id)}
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------- pages
LANDING_FONTS = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap"


def stars(n: int = 5) -> str:
    return '<span class="l-stars" aria-hidden="true">' + icon("star") * n + "</span>"


def enquiry_card(name: str, need: str, when: str, tag: str, tone: str = "") -> str:
    """A small interface card: one enquiry, as it lands in a client's inbox."""
    return f"""<div class="ui-row{' ui-row--' + tone if tone else ''}">
  <span class="ui-row__tick" aria-hidden="true">{icon('check')}</span>
  <div><b>{e(name)}</b><span>{e(need)}</span><i class="ui-chip ui-chip--{tone or 'grey'}">{e(tag)}</i></div>
  <em>{e(when)}</em>
</div>"""


def stat_card(label: str, who: str, stats: list) -> str:
    cells = "".join(f'<div><span>{e(k)}</span><b>{e(v)}<small>{e(of)}</small></b></div>' for k, v, of in stats)
    return f"""<div class="ui-stats">
  <div class="ui-stats__head"><span class="ui-ico">{icon('chart')}</span><div><span>{e(label)}</span><b>{e(who)}</b></div></div>
  <div class="ui-stats__grid">{cells}</div>
</div>"""


def phone(screen: str, cls: str = "") -> str:
    return f"""<div class="ui-phone{(' ' + cls) if cls else ''}" aria-hidden="true">
  <div class="ui-phone__screen"><div class="ui-phone__bar"><b>9:41</b><i></i><span></span></div>{screen}</div>
</div>"""


def landing_page(body: str) -> None:
    L = C["landing"]
    nav = "".join(f'<a href="{e(h)}">{e(n)}</a>' for n, h in L["nav"])
    logo = f'<span class="l-logo__mark">{icon("mark")}</span><span>{e(S["name"])}</span>'
    social_icon = {"LinkedIn": "linkedin", "Instagram": "instagram", "Dribbble": "dribbble"}
    social = "".join(f'<a class="l-social" href="{e(s["href"])}" aria-label="{e(s["label"])}">{icon(social_icon.get(s["label"], "arrow"))}</a>'
                     for s in S["social"])
    addr = ", ".join(S["address"])
    full = f"{S['name']} | {S['tagline']}"
    html_doc = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(S['description'])}">
<link rel="canonical" href="{e(S['url'] + '/')}">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(S['description'])}">
<meta property="og:type" content="website">
<meta property="og:url" content="{e(S['url'] + '/')}">
<meta name="theme-color" content="#1487D2">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%231487D2'/%3E%3Cpath d='M16 5 27 16 16 27 5 16z' fill='%23fff'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{LANDING_FONTS}">
<link rel="stylesheet" href="/assets/css/landing.css">
</head>
<body class="landing">
<a class="l-skip" href="#main">Skip to content</a>
<header class="l-nav">
    <div class="l-wrap l-nav__in">
      <a class="l-logo" href="/" aria-label="{e(S['name'])}, home">{logo}</a>
      <nav class="l-nav__links" aria-label="Main">{nav}</nav>
      <a class="l-btn l-btn--white l-nav__cta" href="/contact/">{e(L['nav_cta'])}</a>
      <details class="l-menu">
        <summary aria-label="Menu"><i></i><i></i><i></i></summary>
        <nav class="l-menu__panel" aria-label="Mobile">{nav}<a href="/work/">Work</a><a href="/studio/">Studio</a><a href="/contact/">Contact</a></nav>
      </details>
    </div>
</header>
{body}
<footer class="l-footer">
  <div class="l-wrap">
    <div class="l-footer__top">
      <div class="l-footer__about"><a class="l-logo" href="/">{logo}</a><p>{e(L['footer_text'])}</p></div>
      <div class="l-footer__contact">
        <div class="l-footer__col">
          <h2>Get in touch</h2>
          <a href="mailto:{e(S['email'])}">{e(S['email'])}</a>
          <a href="tel:{S['phone_href']}">{e(S['phone'])}</a>
          <span>{e(addr)}</span>
        </div>
        <div class="l-footer__col">
          <h2>Follow us</h2>
          <div class="l-footer__social">{social}</div>
        </div>
      </div>
    </div>
    <div class="l-footer__bottom">
      <a class="l-footer__big" href="/" aria-label="{e(S['name'])}, home"><span class="l-logo__mark">{icon("mark")}</span><span>{e(S['name'])}</span></a>
      <div class="l-footer__info">
        <div class="l-footer__links"><a href="/work/">Work</a><i></i><a href="/studio/">Studio</a><i></i><a href="/privacy/">Privacy</a></div>
        <p>© {date.today().year} {e(S['name'])} Ltd.</p>
      </div>
    </div>
  </div>
</footer>
<script src="/assets/js/landing.js" defer></script>
</body>
</html>
"""
    (SITE / "index.html").write_text(html_doc, encoding="utf-8")


def build_home() -> None:
    L = C["landing"]

    # hero visual: a phone showing new enquiries, with two cards floating off it
    inbox = ('<p class="ui-title">New enquiries</p><p class="ui-sub">This week</p>'
             + enquiry_card("Emma Clarke", "Check-up and clean", "Mon", "Booked", "green")
             + enquiry_card("Tom Reid", "Boiler repair", "Mon", "Urgent", "red")
             + enquiry_card("Priya Shah", "Kitchen extension", "Tue", "Quote sent")
             + enquiry_card("Mark Owen", "Roof inspection", "Wed", "Call back")
             + enquiry_card("Sara Lin", "Teeth whitening", "Thu", "Booked", "green"))
    hero_visual = f"""<div class="l-hero__visual" aria-hidden="true">
  {phone(inbox + '<div class="ui-phone__tab"><span></span><b>Enquiries</b><span></span><span></span></div>')}
  <div class="l-float l-float--stats">{stat_card('This month', 'Bright Smile Dental', [('Calls', '48', '/40'), ('Forms', '31', '/25'), ('Bookings', '22', '/20')])}</div>
  <div class="l-float l-float--row">{enquiry_card('Website form', 'Emergency call-out', 'Now', 'New lead', 'red')}</div>
</div>"""

    logo_cells = "".join(f'<li>{ph(f"Client logo {i + 1}", "l-logo-ph")}</li>' for i in range(L["logos"]))
    avatars = "".join(f'<span class="l-avatar l-avatar--{i}"></span>' for i in range(4))
    a, b, c = L["card_a"], L["card_b"], L["card_c"]

    s1, s2, s3, s4 = L["services"]
    def svc_content(s: dict, large: bool = False) -> str:
        return f"""<div class="l-feature__content{' is-large' if large else ''}">
  <span class="l-feature__icon">{icon(s['icon'])}</span>
  <h3>{e(s['title'])}</h3>
  <p>{e(s['text'])}</p>
</div>"""
    v1 = ('<div class="ui-stack">' + enquiry_card("Homepage", "Concept A", "Mon", "In review")
          + enquiry_card("Services page", "Concept B", "Tue", "Approved", "green")
          + enquiry_card("Booking page", "Mobile first", "Wed", "Next up") + '</div>')
    v2 = (phone('<p class="ui-hello">Bright Smile Dental</p><div class="ui-site"><span></span><span></span><span></span></div>'
                '<div class="ui-cta">Book an appointment</div>', "ui-phone--crop")
          + '<div class="l-float l-float--timer"><span class="ui-ico">' + icon("phone") + '</span><div><span>Calls this week</span><b>48</b></div></div>')
    v3 = stat_card("Results this month", "Reid Plumbing & Heating", [("Calls", "36", "/30"), ("Forms", "19", "/15"), ("Bookings", "14", "/12")])
    v4 = (phone('<p class="ui-title">Google profile</p><p class="ui-sub">Owen Roofing</p>'
                + enquiry_card("New review", "★★★★★", "1h", "5.0", "green")
                + enquiry_card("Map views", "+64% this month", "Now", "Up")
                + enquiry_card("Website clicks", "From local search", "Today", "Up"), "ui-phone--crop")
          + f'<div class="l-float l-float--reviews"><span class="ui-ico">{icon("star")}</span>{avatars}</div>')

    step_cards = "".join(f"""<li class="l-step{' is-first' if i == 0 else ''}">
  <div class="l-step__left">
    <span class="l-pill l-pill--mint">Step {i + 1}</span>
    <div class="l-step__content"><h3>{e(st['title'])}</h3><p>{e(st['text'])}</p></div>
  </div>
  {('<div class="l-step__img">' + ph('Example of a recorded website review', '') + '</div>') if i == 0 else ''}
</li>""" for i, st in enumerate(L["steps"]))

    posts = sorted(C["journal"], key=lambda p: p["date"], reverse=True)
    slides = "".join(f"""<li class="l-post">
  <a href="/journal/{e(p['slug'])}/">
    <div class="l-post__img">{ph(f"Cover image for {p['title']}", '')}<span class="l-pill l-pill--mint">{nice_date(p['date'])}</span></div>
    <div class="l-post__content"><h3>{e(p['title'])}</h3><p>{e(p['lede'])}</p></div>
  </a>
</li>""" for p in posts)

    body = f"""<main id="main">
  <section class="l-hero" aria-labelledby="hero-h">
    <div class="l-wrap l-hero__layout">
      <div class="l-hero__left">
        <div class="l-hero__top">
          <span class="l-pill l-pill--glass">{e(L['tag'])}</span>
          <h1 id="hero-h">{e(L['title'])}</h1>
          <p class="l-hero__lede">{e(L['lede'])}</p>
          <div class="l-hero__buttons">
            <a class="l-btn l-btn--icon" href="/contact/">{e(L['primary'])}<span>{icon('right')}</span></a>
            <a class="l-btn l-btn--dark" href="/work/">{e(L['secondary'])}</a>
          </div>
        </div>
        <div class="l-rating">{stars()}<span>{e(L['rating'])}</span></div>
      </div>
      {hero_visual}
    </div>
  </section>

<section class="l-loop" aria-label="Clients">
  <div class="l-wrap l-loop__layout">
    <p class="l-loop__text">{e(L['trusted'][0])}<br>{e(L['trusted'][1])}</p>
    <div class="l-loop__track">
      <ul class="l-loop__row">{logo_cells}</ul><ul class="l-loop__row" aria-hidden="true">{logo_cells}</ul>
      <span class="l-loop__fade l-loop__fade--l"></span><span class="l-loop__fade l-loop__fade--r"></span>
    </div>
  </div>
</section>

<section class="l-section" id="results" aria-labelledby="results-h">
  <div class="l-wrap">
    <div class="l-head l-head--split">
      <div><span class="l-pill">{e(L['results_tag'])}</span><h2 id="results-h">{e(L['results_title'][0])}<br>{e(L['results_title'][1])}</h2></div>
      <p>{e(L['results_lede'])}</p>
    </div>
    <div class="l-impacts">
      <div class="l-impacts__col">
        <div class="l-card l-card--short"><span class="l-avatars">{avatars}</span><span class="l-caps">{e(L['trust_line'])}</span></div>
        <div class="l-card l-card--medium"><p class="l-card__lead">{e(a['text'])}</p>
          <div><p class="l-num">{e(a['value'])}<span>{e(a['suffix'])}</span></p><p class="l-card__cap">{e(a['caption'])}</p></div></div>
      </div>
      <div class="l-card l-card--dark"><p class="l-card__lead">{e(b['text'])}</p>
        <div class="l-card__rate"><p class="l-num">{e(b['value'])}<span>{e(b['suffix'])}</span></p><div>{stars()}<p>{e(b['caption'])}</p></div></div></div>
      <div class="l-impacts__col">
        <div class="l-card l-card--medium"><p class="l-card__lead">{e(c['text'])}</p>
          <div><p class="l-num">{e(c['value'])}<span>{e(c['suffix'])}</span></p><p class="l-card__cap">{e(c['caption'])}</p></div></div>
        <div class="l-card l-card--short"><span class="l-feature__icon l-feature__icon--sm">{icon('phone')}</span><span class="l-caps">{e(L['fast_line'])}</span></div>
      </div>
    </div>
  </div>
</section>

<section class="l-section" id="services" aria-labelledby="services-h">
  <div class="l-wrap">
    <div class="l-head l-head--center">
      <span class="l-pill">{e(L['services_tag'])}</span>
      <h2 id="services-h">{e(L['services_title'])}</h2>
      <p>{e(L['services_lede'])}</p>
    </div>
    <div class="l-features">
      <article class="l-feature is-large"><div class="l-visual" aria-hidden="true">{v1}</div>{svc_content(s1, True)}</article>
      <article class="l-feature"><div class="l-visual l-visual--short" aria-hidden="true">{v2}</div>{svc_content(s2)}</article>
      <article class="l-feature"><div class="l-visual l-visual--short" aria-hidden="true">{v3}</div>{svc_content(s3)}</article>
      <article class="l-feature is-large"><div class="l-visual" aria-hidden="true">{v4}</div>{svc_content(s4, True)}</article>
    </div>
  </div>
</section>

<section class="l-section" id="how" aria-labelledby="how-h">
  <div class="l-wrap">
    <div class="l-head l-head--center">
      <span class="l-pill">{e(L['steps_tag'])}</span>
      <h2 id="how-h">{e(L['steps_title'])}</h2>
      <p>{e(L['steps_lede'])}</p>
    </div>
    <ol class="l-steps">{step_cards}</ol>
  </div>
</section>

<section class="l-section l-section--journal" id="journal" aria-labelledby="journal-h">
  <div class="l-wrap">
    <div class="l-head">
      <span class="l-pill">{e(L['journal_tag'])}</span>
      <h2 id="journal-h">{e(L['journal_title'])}</h2>
      <div class="l-head__bottom"><p>{e(L['journal_lede'])}</p>
        <div class="l-arrows"><button type="button" class="l-arrow" data-dir="-1" aria-label="Previous articles">{icon('left')}</button><button type="button" class="l-arrow" data-dir="1" aria-label="Next articles">{icon('right')}</button></div>
      </div>
    </div>
  </div>
  <ul class="l-posts" tabindex="0" aria-label="Journal articles">{slides}</ul>
</section>
</main>"""
    landing_page(body)


def build_work_index() -> None:
    body = f"""
<section class="page-hero">
  <div class="wrap page-hero__row">
    <h1 data-r>Every project<br><span class="acc">we’ve launched.</span></h1>
    <p class="page-hero__side" data-r="120">{len(C['work'])} projects, each measured against the same months the year before. Reported in enquiries, bookings and calls.</p>
  </div>
</section>
<section class="band" style="padding-top:0">
  <div class="wrap">{work_grid(C['work'])}</div>
</section>
"""
    page("/work/", "Work", "Websites Quincy Lou has designed, built and optimised, with the numbers behind each one.", body, "Work")


def build_case_studies() -> None:
    work = C["work"]
    for i, w in enumerate(work):
        nxt = work[(i + 1) % len(work)]
        stats = "".join(f'<div class="stat" data-r="{j * 80}"><b>{e(v)}</b><span>{e(k)}</span></div>'
                        for j, (v, k) in enumerate(w["stats"]))
        body = f"""
<section class="page-hero">
  <div class="wrap">
    <a class="back" href="/work/">{icon('back')}All work</a>
    <div class="cs-title" data-r><h1>{e(w['name'])}<span class="acc">{e(w['line'])}</span></h1></div>
    <dl class="meta" data-r="120">
      <div><dt>Year</dt><dd>{e(w['year'])}</dd></div>
      <div><dt>Service</dt><dd>{e(w['service'])}</dd></div>
      <div><dt>Industry</dt><dd>{e(w['industry'])}</dd></div>
      <div><dt>Result</dt><dd class="red">{e(w['result'])}</dd></div>
    </dl>
  </div>
</section>
<section><div class="wrap" data-r>{ph(f"{w['name']} hero image", "ph--reel")}</div></section>
<section class="band">
  <div class="wrap cs-body">
    <h2 data-r>The short <span class="acc">version.</span></h2>
    <div class="cs-parts">
      <div data-r><h3>The problem</h3><p>{e(w['challenge'])}</p></div>
      <div data-r><h3>What we did</h3><p>{e(w['approach'])}</p></div>
      <div data-r><h3>What changed</h3><p>{e(w['outcome'])}</p></div>
    </div>
  </div>
</section>
<section class="band" style="padding-top:0"><div class="wrap stats">{stats}</div></section>
<section class="band" style="padding-top:0">
  <div class="wrap gallery">
    <div class="wide" data-r>{ph(f"{w['name']} homepage on desktop", "ph--r169")}</div>
    <div data-r>{ph(f"{w['name']} on a phone", "ph--r45")}</div>
    <div data-r="100">{ph(f"{w['name']} detail", "ph--r45")}</div>
  </div>
</section>
<section class="band" style="padding-top:0">
  <div class="wrap">
    <figure class="cs-quote" data-r>
      <blockquote>{e(w['quote'])}</blockquote>
      <figcaption class="who">{ph('Client photo', 'ph--avatar')}<span><b>Client name</b><span>Role, {e(w['name'])}</span></span></figcaption>
    </figure>
  </div>
</section>
<section class="band" style="padding-top:0">
  <div class="wrap">
    <a class="next" href="/work/{e(nxt['slug'])}/"><div><span>Next project</span><b>{e(nxt['name'])}</b></div>{icon('next')}</a>
  </div>
</section>
{enquire_block()}
"""
        page(f"/work/{w['slug']}/", w["name"], f"{w['name']}: {w['line']}. {w['result']}.", body, "Work")


def build_studio() -> None:
    st = C["studio"]
    ways = "".join(f"""<div class="way" data-r="{i * 80}"><span>0{i + 1}</span><h3>{e(w['title'])}</h3><p>{e(w['text'])}</p></div>"""
                   for i, w in enumerate(st["ways"]))
    beliefs = "".join(f'<li data-r>{icon("asterisk")}<span>{e(b)}</span></li>' for b in st["beliefs"])
    hire = st["hiring"]
    body = f"""
<section class="page-hero">
  <div class="wrap page-hero__row">
    {acc_title(st['title'], 'h1', ' data-r')}
    <p class="page-hero__side" data-r="120">{e(st['lede'])}</p>
  </div>
</section>
<section>
  <div class="wrap"><div class="studio-shot" data-r>{ph('The team in the studio', 'ph--studio')}<span class="place-tag">{icon('asterisk')}{e(st['place'])}</span></div></div>
</section>
<section class="band ways-band"><div class="wrap ways">{ways}</div></section>
<section class="band team-band" style="padding-top:0">
  <div class="wrap">
    <div class="head">{acc_title(C['home']['team_title'], 'h2', ' data-r')}</div>
    {team_block()}
  </div>
</section>
<section class="band beliefs-band" style="padding-top:0" aria-labelledby="beliefs-h">
  <div class="wrap">
    <p class="beliefs__label" id="beliefs-h">{e(st['beliefs_label'])}</p>
    <ul class="beliefs">{beliefs}</ul>
  </div>
</section>
<section class="hiring-band">
  <div class="wrap">
    <div class="hiring" data-r>
      <div><h2>{e(hire['title'])}</h2><p>{e(hire['text'])}</p></div>
      {btn(hire['cta'], 'mailto:' + S['email'], 'cta')}
    </div>
  </div>
</section>
"""
    page("/studio/", "Studio", "Quincy Lou is a small website studio for service businesses. Four people, no middlemen.", body, "Studio")


def build_journal() -> None:
    posts = sorted(C["journal"], key=lambda p: p["date"], reverse=True)
    f, rest = posts[0], posts[1:]
    grid = "".join(post_card(p, i) for i, p in enumerate(rest))
    body = f"""
<section class="page-hero">
  <div class="wrap page-hero__row">
    <h1 data-r>Notes from<br><span class="acc">the studio.</span></h1>
    <p class="page-hero__side" data-r="120">Short, practical pieces on what makes a service business website bring in more work.</p>
  </div>
</section>
<section class="band" style="padding-top:0">
  <div class="wrap">
    <a class="feature" href="/journal/{e(f['slug'])}/" data-r>
      {ph(f"Cover image for {f['title']}", "ph--r43")}
      <div>
        <div class="post__meta"><span class="chip-ink">{e(f['tag'])}</span><span>{nice_date(f['date'])}</span></div>
        <h2>{e(f['title'])}</h2>
        <p>{e(f['lede'])}</p>
      </div>
    </a>
    <div class="posts posts--two">{grid}</div>
  </div>
</section>
"""
    page("/journal/", "Journal", "Practical notes on websites for service businesses, from the Quincy Lou studio.", body, "Journal")


def build_articles() -> None:
    posts = sorted(C["journal"], key=lambda p: p["date"], reverse=True)
    for p in posts:
        blocks = []
        for kind, val in p["body"]:
            if kind == "p":
                blocks.append(f"<p>{e(val)}</p>")
            elif kind == "h2":
                blocks.append(f"<h2>{e(val)}</h2>")
            elif kind == "list":
                blocks.append("<ul>" + "".join(f"<li>{e(x)}</li>" for x in val) + "</ul>")
        more = "".join(post_card(q, i) for i, q in enumerate([q for q in posts if q["slug"] != p["slug"]][:3]))
        body = f"""
<article>
  <section class="page-hero">
    <div class="wrap">
      <a class="back" href="/journal/">{icon('back')}All articles</a>
      <div class="article-head" data-r>
        <div class="post__meta"><span class="chip-ink">{e(p['tag'])}</span><span>{nice_date(p['date'])} · {e(p['read'])} read</span></div>
        <h1>{e(p['title'])}</h1>
        <p class="lede">{e(p['lede'])}</p>
      </div>
    </div>
  </section>
  <div class="wrap" data-r>{ph(f"Cover image for {p['title']}", "ph--reel")}</div>
  <div class="wrap band">
    <div class="prose">{''.join(blocks)}</div>
    <div class="share"><span>Written by the Quincy Lou studio</span><a href="/contact/">Want us to look at your site?</a></div>
  </div>
</article>
<section class="band" style="padding-top:0">
  <div class="wrap">
    <div class="head"><h2>Keep <span class="acc">reading.</span></h2>{btn('All articles', '/journal/', 'line')}</div>
    <div class="posts">{more}</div>
  </div>
</section>
"""
        page(f"/journal/{p['slug']}/", p["title"], p["lede"], body, "Journal")


def build_contact() -> None:
    ct = C["contact"]
    faq = "".join(f"""<details class="qa"{' open' if i == 0 else ''}><summary>{e(q)}<i aria-hidden="true"></i></summary><p>{e(a)}</p></details>"""
                  for i, (q, a) in enumerate(ct["faq"]))
    body = f"""
{enquire_block('contact', 'h1', 'band contact-top')}
<section class="band faq-band" aria-labelledby="faq-h">
  <div class="wrap faq-grid">
    <div class="faq-grid__head">
      {acc_title(ct['faq_title'], 'h2', ' id="faq-h" data-r')}
      <p data-r="100">{e(ct['faq_lede'])}</p>
    </div>
    <div class="qas" data-r="120">{faq}</div>
  </div>
</section>
"""
    page("/contact/", "Contact", "Get in touch with Quincy Lou for a free website review. We reply within one working day.", body)


def build_privacy() -> None:
    pv = C["privacy"]
    secs = "".join(f"<section><h2>{e(h)}</h2><p>{e(t)}</p></section>" for h, t in pv["sections"])
    body = f"""
<section class="page-hero">
  <div class="wrap page-hero__row">
    <h1 data-r>Privacy<br><span class="acc">policy.</span></h1>
    <p class="page-hero__side" data-r="120">Last updated {e(pv['updated'])}. Plain English, as short as we could make it.</p>
  </div>
</section>
<section class="band" style="padding-top:0"><div class="wrap legal">{secs}
  <section><h2>Contact</h2><p>Questions about this policy: <a href="mailto:{e(S['email'])}">{e(S['email'])}</a>. {e(S['company'])}</p></section>
</div></section>
"""
    page("/privacy/", "Privacy", "How Quincy Lou collects and uses personal information.", body)


def build_thanks() -> None:
    body = f"""
<section class="page-hero"><div class="wrap lost">
  <h1>Thank<br><span class="acc">you.</span></h1>
  <p class="hero__lede">Your message is with us. {e(S['reply_time'])}, usually much sooner.</p>
  <div class="hero__ctas">{btn('Back to the homepage', '/', 'cta')}{btn('Read the journal', '/journal/', 'line')}</div>
</div></section>
"""
    page("/thanks/", "Thank you", "Thanks for getting in touch with Quincy Lou.", body)


def build_404() -> None:
    body = f"""
<section class="page-hero"><div class="wrap lost">
  <h1>Page<br><span class="acc">not found.</span></h1>
  <p class="hero__lede">That link has moved or never existed. The useful parts of the site are one click away.</p>
  <div class="hero__ctas">{btn('Go to the homepage', '/', 'cta')}{btn('See our work', '/work/', 'line')}</div>
</div></section>
"""
    page("/404", "Page not found", "This page could not be found.", body)


def clean() -> None:
    """Remove previously generated pages, keeping assets/."""
    keep = {"assets"}
    for child in SITE.iterdir():
        if child.name in keep:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        elif child.suffix == ".html" or child.name in {"sitemap.xml", "robots.txt"}:
            child.unlink()


def build_sitemap(paths: list[str]) -> None:
    urls = "".join(f"<url><loc>{e(S['url'] + p)}</loc></url>" for p in paths)
    (SITE / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',
        encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {S['url']}/sitemap.xml\n", encoding="utf-8")


def main() -> None:
    SITE.mkdir(exist_ok=True)
    clean()
    build_home()
    build_work_index()
    build_case_studies()
    build_studio()
    build_journal()
    build_articles()
    build_contact()
    build_privacy()
    build_thanks()
    build_404()
    paths = (["/", "/work/", "/studio/", "/journal/", "/contact/", "/privacy/"]
             + [f"/work/{w['slug']}/" for w in C["work"]]
             + [f"/journal/{p['slug']}/" for p in C["journal"]])
    build_sitemap(paths)
    count = len(list(SITE.glob("**/index.html")))
    print(f"Built {count} pages + 404 into {SITE.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
