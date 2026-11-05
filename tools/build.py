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


def ph(label: str, cls: str = "ph--r43", extra: str = "") -> str:
    """A blank image placeholder that still tells a screen reader what belongs there."""
    return f'<span class="ph {cls}{" " + extra if extra else ""}" role="img" aria-label="{e(label)}"></span>'


def nice_date(iso: str) -> str:
    d = date.fromisoformat(iso)
    return d.strftime("%-d %b %Y")


# ------------------------------------------------------------- page chrome
FONTS = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap"


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


def page(path: str, title: str, desc: str, body: str, *, home: bool = False, review: bool = True) -> None:
    """Write one page: head, navigation, the page body, footer.

    home:   the homepage, whose navigation sits over the blue hero panel.
    review: the page carries the free-review form (id="review"), so the
            navigation button can jump to it; other pages link to the contact page.
    """
    L = C["landing"]
    pre = "" if home else "/"
    links = [(n, (pre + h) if h.startswith("#") else h) for n, h in L["nav"]]
    nav = "".join(f'<a href="{e(h)}">{e(n)}</a>' for n, h in links)
    cta = "#review" if review else "/contact/"
    logo = f'<span class="l-logo__mark">{icon("mark")}</span><span>{e(S["name"])}</span>'
    social_icon = {"LinkedIn": "linkedin", "Instagram": "instagram", "Dribbble": "dribbble"}
    social = "".join(f'<a class="l-social" href="{e(s["href"])}" aria-label="{e(s["label"])}">{icon(social_icon.get(s["label"], "arrow"))}</a>'
                     for s in S["social"])
    addr = ", ".join(S["address"])
    full = f"{S['name']} | {S['tagline']}" if home else f"{title} | {S['name']}"
    url = S["url"] + ("/" if path == "/" else path)
    html_doc = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(url)}">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{e(url)}">
<meta name="theme-color" content="{'#1487D2' if home else '#F7F7F7'}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%231487D2'/%3E%3Cpath d='M16 5 27 16 16 27 5 16z' fill='%23fff'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/css/site.css">
</head>
<body class="page">
<a class="l-skip" href="#main">Skip to content</a>
<header class="l-nav{'' if home else ' l-nav--light'}">
    <div class="l-wrap l-nav__in">
      <a class="l-logo" href="/" aria-label="{e(S['name'])}, home">{logo}</a>
      <nav class="l-nav__links" aria-label="Main">{nav}</nav>
      <a class="l-btn {'l-btn--white' if home else 'l-btn--dark'} l-nav__cta" href="{cta}">{e(L['nav_cta'])}</a>
      <details class="l-menu">
        <summary aria-label="Menu"><i></i><i></i><i></i></summary>
        <nav class="l-menu__panel" aria-label="Mobile">{nav}<a href="/work/">Work</a><a href="/journal/">Journal</a><a href="/studio/">Studio</a><a href="/contact/">Contact</a></nav>
      </details>
    </div>
</header>
<main id="main">
{body}
</main>
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
        <div class="l-footer__links"><a href="/work/">Work</a><i></i><a href="/studio/">Studio</a><i></i><a href="/journal/">Journal</a><i></i><a href="/contact/">Contact</a><i></i><a href="/privacy/">Privacy</a></div>
        <p>© {date.today().year} {e(S['company'])}</p>
      </div>
    </div>
  </div>
</footer>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""
    out = SITE / "404.html" if path == "/404" else SITE / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc, encoding="utf-8")


# --------------------------------------------------------- shared sections
def sector_of(w: dict) -> str:
    """The industry filter a project sits under."""
    return C["landing"]["case_sectors"].get(w["slug"], w["industry"])


def review_form(name: str = "website-review") -> str:
    L = C["landing"]
    sector_opts = "".join(f'<option>{e(x)}</option>' for x in L["cta_sectors"])
    return f"""<form class="l-form" name="{name}" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="company-website">
      <input type="hidden" name="form-name" value="{name}">
      <p class="l-hp" aria-hidden="true"><label>Leave this empty <input name="company-website" tabindex="-1" autocomplete="off"></label></p>
      <div class="l-form__row">
        <label><span>Your name</span><input name="name" autocomplete="name" required></label>
        <label><span>Email</span><input type="email" name="email" autocomplete="email" required></label>
      </div>
      <label><span>Your website</span><input type="url" name="website" placeholder="https://" inputmode="url"></label>
      <label><span>Type of business</span><select name="business" required><option value="">Choose one</option>{sector_opts}</select></label>
      <label><span>Anything we should know? <em>(optional)</em></span><textarea name="message" rows="3" placeholder="What would a good month of enquiries look like?"></textarea></label>
      <button class="l-btn l-btn--dark l-form__submit" type="submit">{e(L['cta_button'])}</button>
      <p class="l-form__note">{e(S['reply_time'])}. No newsletter unless you ask for it.</p>
    </form>"""


def cta_block() -> str:
    """The blue free-review panel that closes most pages."""
    L = C["landing"]
    points = "".join(f'<li>{icon("check")}{e(x)}</li>' for x in L["cta_points"])
    return f"""<section class="l-cta" id="review" aria-labelledby="review-h">
  <div class="l-wrap l-cta__layout">
    <div class="l-cta__copy">
      <span class="l-pill l-pill--glass">{e(L['cta_tag'])}</span>
      <h2 id="review-h">{e(L['cta_title'])}</h2>
      <p>{e(L['cta_text'])}</p>
      <ul class="l-cta__points">{points}</ul>
    </div>
    {review_form()}
  </div>
</section>"""


def cta_band(title: str, text: str) -> str:
    """A short dark strip with one button, for the middle of a long page."""
    return f"""<div class="l-band">
  <div><h3>{e(title)}</h3><p>{e(text)}</p></div>
  <a class="l-btn l-btn--icon" href="#review">{e(C['landing']['primary'])}<span>{icon('right')}</span></a>
</div>"""


def case_card(w: dict) -> str:
    sector = sector_of(w)
    return f"""<li class="l-case" data-sector="{e(sector)}">
  <a href="/work/{e(w['slug'])}/">
    <div class="l-case__img">{ph(f"{w['name']} website", '')}<span class="l-pill l-pill--mint">{e(sector)}</span></div>
    <div class="l-case__body">
      <p class="l-case__num">{e(w['stats'][0][0])}<span>{e(w['stats'][0][1])}</span></p>
      <h3>{e(w['name'])}</h3><p>{e(w['line'])}</p>
      <span class="l-case__more">Read the case study{icon('right')}</span>
    </div>
  </a>
</li>"""


def case_filters(items: list) -> str:
    order = ["Dental & health", "Home services", "Construction"]
    found = {sector_of(w) for w in items}
    sectors = [s for s in order if s in found] + sorted(found - set(order))
    btns = "".join(f'<button type="button" class="l-filter{" is-on" if f == "All" else ""}" data-filter="{e(f)}" aria-pressed="{"true" if f == "All" else "false"}">{e(f)}</button>'
                   for f in ["All"] + sectors)
    return f'<div class="l-filters" role="group" aria-label="Filter case studies by industry">{btns}</div>'


def post_card(p: dict) -> str:
    return f"""<li class="l-case l-case--post">
  <a href="/journal/{e(p['slug'])}/">
    <div class="l-case__img l-case__img--blue">{ph(f"Cover image for {p['title']}", '')}<span class="l-pill l-pill--mint">{nice_date(p['date'])}</span></div>
    <div class="l-case__body">
      <h3>{e(p['title'])}</h3><p>{e(p['lede'])}</p>
      <span class="l-case__more">Read the article{icon('right')}</span>
    </div>
  </a>
</li>"""


def list_head(tag: str, title: str, lede: str, extra: str = "") -> str:
    """The opening of a listing page: label, big title, a short line and optional controls."""
    return f"""<div class="l-head l-head--page">
      <span class="l-pill">{e(tag)}</span>
      <h1 id="page-h">{e(title)}</h1>
      <div class="l-head__bottom"><p>{e(lede)}</p>{extra}</div>
    </div>"""


def doc_head(tags: str, title: str, lede: str, image: str = "", meta: str = "") -> str:
    """The opening of a single article or project: a centred white card, like a document cover."""
    img = f'<div class="l-doc__img">{image}</div>' if image else ""
    met = f'<div class="l-doc__meta">{meta}</div>' if meta else ""
    return f"""<header class="l-doc__head">
      <div class="l-doc__title"><div class="l-doc__tags">{tags}</div><h1>{e(title)}</h1><p>{e(lede)}</p></div>
      {img}{met}
    </header>"""


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

    problems = "".join(f"""<li class="l-card l-problem">
  <span class="l-feature__icon">{icon(p['icon'])}</span><h3>{e(p['title'])}</h3><p>{e(p['text'])}</p>
</li>""" for p in L["problems"])

    cases = [w for w in C["work"] if w["slug"] in L["case_sectors"]]
    case_cards = "".join(case_card(w) for w in cases)

    industries = "".join(f"""<li class="l-industry">
  <div class="l-industry__img">{ph(f"{x['title']} website example", '')}</div>
  <div class="l-industry__body">
    <h3>{e(x['title'])}</h3><p>{e(x['problem'])}</p>
    <div class="l-industry__foot"><span class="l-pill l-pill--mint">{e(x['result'])}</span>
      <a class="l-link" href="#work" data-set-filter="{e(x['filter'])}">See the work{icon('right')}</a></div>
  </div>
</li>""" for x in L["industries"])

    facts = "".join(f'<li><b>{e(v)}</b><span>{e(k)}</span></li>' for v, k in L["founder_facts"])

    voices = "".join(f"""<li class="l-card l-voice">
  <p class="l-voice__num">{e(v['metric'])}<span>{e(v['label'])}</span></p>
  <blockquote>{e(v['quote'])}</blockquote>
  <div class="l-voice__who">{ph('Client photo', 'l-voice__photo')}<div><b>{e(v['name'])}</b><span>{e(v['role'])}</span></div></div>
</li>""" for v in L["voices"])

    def mark(v: str) -> str:
        if v == "yes":
            return f'<span class="l-yes">{icon("check")}<span class="sr">Yes</span></span>'
        if v == "no":
            return '<span class="l-no" aria-label="No">–</span>'
        return e(v)
    cols = L["compare_cols"]
    us = ' class="is-us"'
    compare_head = "".join(f'<th scope="col"{us if i == 0 else ""}>{e(c)}</th>' for i, c in enumerate(cols))
    compare_rows = "".join('<tr><th scope="row">' + e(r[0]) + "</th>"
                           + "".join(f'<td{us if i == 0 else ""} data-label="{e(cols[i])}">{mark(v)}</td>' for i, v in enumerate(r[1:]))
                           + "</tr>" for r in L["compare_rows"])

    plans = "".join(f"""<li class="l-plan{' is-featured' if p['featured'] else ''}">
  <div class="l-plan__top"><h3>{e(p['name'])}</h3>{('<span class="l-pill l-pill--mint">' + e(p['badge']) + '</span>') if p.get('badge') else ''}</div>
  <p class="l-plan__price">{e(p['price'])}<span>{e(p['unit'])}</span></p>
  <p class="l-plan__text">{e(p['text'])}</p>
  <ul>{''.join(f'<li>{icon("check")}{e(i)}</li>' for i in p['items'])}</ul>
  <a class="l-btn {'l-btn--icon' if p['featured'] else 'l-btn--dark'}" href="#review">{e(p['cta'])}{('<span>' + icon('right') + '</span>') if p['featured'] else ''}</a>
</li>""" for p in C["pricing"])

    faq = "".join(f"""<details class="l-qa"{' open' if i == 0 else ''}><summary>{e(q)}<i aria-hidden="true"></i></summary><p>{e(a_)}</p></details>"""
                  for i, (q, a_) in enumerate(L["faq"]))


    body = f"""
  <section class="l-hero" aria-labelledby="hero-h">
    <div class="l-wrap l-hero__layout">
      <div class="l-hero__left">
        <div class="l-hero__top">
          <span class="l-pill l-pill--glass">{e(L['tag'])}</span>
          <h1 id="hero-h">{e(L['title'])}</h1>
          <p class="l-hero__lede">{e(L['lede'])}</p>
          <div class="l-hero__buttons">
            <a class="l-btn l-btn--icon" href="#review">{e(L['primary'])}<span>{icon('right')}</span></a>
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

<section class="l-section" id="problem" aria-labelledby="problem-h">
  <div class="l-wrap">
    <div class="l-head l-head--center">
      <span class="l-pill">{e(L['problem_tag'])}</span>
      <h2 id="problem-h">{e(L['problem_title'])}</h2>
      <p>{e(L['problem_lede'])}</p>
    </div>
    <ul class="l-problems">{problems}</ul>
  </div>
</section>

<section class="l-section" id="industries" aria-labelledby="industries-h">
  <div class="l-wrap">
    <div class="l-head l-head--center">
      <span class="l-pill">{e(L['industries_tag'])}</span>
      <h2 id="industries-h">{e(L['industries_title'])}</h2>
    </div>
    <ul class="l-industries">{industries}</ul>
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

<section class="l-section" id="work" aria-labelledby="work-h">
  <div class="l-wrap">
    <div class="l-head">
      <span class="l-pill">{e(L['cases_tag'])}</span>
      <h2 id="work-h">{e(L['cases_title'])}</h2>
      <div class="l-head__bottom"><p>{e(L['cases_lede'])}</p>
        {case_filters(cases)}</div>
    </div>
    <ul class="l-cases">{case_cards}</ul>
    <div class="l-center"><a class="l-btn l-btn--dark" href="/work/">See all projects</a></div>
  </div>
</section>

<section class="l-section l-section--band" aria-label="Free review">
  <div class="l-wrap">{cta_band(L['band_title'], L['band_text'])}</div>
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

<section class="l-section" id="testimonials" aria-labelledby="voices-h">
  <div class="l-wrap">
    <div class="l-head l-head--split">
      <div><span class="l-pill">{e(L['voices_tag'])}</span><h2 id="voices-h">{e(L['voices_title'])}</h2></div>
      <p class="l-google">{stars()}<span>{e(L['google_rating'])}</span></p>
    </div>
    <ul class="l-voices">{voices}</ul>
  </div>
</section>

<section class="l-section" id="compare" aria-labelledby="compare-h">
  <div class="l-wrap">
    <div class="l-head l-head--center">
      <span class="l-pill">{e(L['compare_tag'])}</span>
      <h2 id="compare-h">{e(L['compare_title'])}</h2>
    </div>
    <div class="l-compare" tabindex="0" role="region" aria-labelledby="compare-h">
      <table><thead><tr><td></td>{compare_head}</tr></thead><tbody>{compare_rows}</tbody></table>
    </div>
  </div>
</section>

<section class="l-section" id="pricing" aria-labelledby="pricing-h">
  <div class="l-wrap">
    <div class="l-head l-head--center">
      <span class="l-pill">{e(L['pricing_tag'])}</span>
      <h2 id="pricing-h">{e(L['pricing_title'])}</h2>
      <p>{e(L['pricing_lede'])}</p>
    </div>
    <ul class="l-plans">{plans}</ul>
    <div class="l-card l-guarantee"><span class="l-feature__icon">{icon('check')}</span><div><h3>{e(L['guarantee_title'])}</h3><p>{e(L['guarantee_text'])}</p></div></div>
  </div>
</section>

<section class="l-section" id="founder" aria-labelledby="founder-h">
  <div class="l-wrap">
    <div class="l-founder">
      <div class="l-founder__img">{ph(f"Photo of {L['founder_name']}", '')}</div>
      <div class="l-founder__body">
        <span class="l-pill l-pill--grey">{e(L['founder_tag'])}</span>
        <h2 id="founder-h">{e(L['founder_title'])}</h2>
        <p>{e(L['founder_text'])}</p>
        <p class="l-founder__sig"><b>{e(L['founder_name'])}</b><span>{e(L['founder_role'])}</span></p>
        <ul class="l-founder__facts">{facts}</ul>
        <a class="l-btn l-btn--dark" href="#review">{e(L['founder_cta'])}</a>
      </div>
    </div>
  </div>
</section>

<section class="l-section" id="faq" aria-labelledby="faq-h">
  <div class="l-wrap l-faq">
    <div class="l-faq__head">
      <span class="l-pill">{e(L['faq_tag'])}</span>
      <h2 id="faq-h">{e(L['faq_title'])}</h2>
      <p>{e(L['faq_lede'])}</p>
    </div>
    <div class="l-qas">{faq}</div>
  </div>
</section>

{cta_block()}
"""
    page("/", S["name"], S["description"], body, home=True)


def build_work_index() -> None:
    work = C["work"]
    body = f"""<section class="l-section l-section--first" aria-labelledby="page-h">
  <div class="l-wrap">
    {list_head('Case studies', 'Every project we have launched.', f"{len(work)} projects, each measured against the same months the year before. Reported in calls, bookings and enquiries.", case_filters(work))}
    <ul class="l-cases">{''.join(case_card(w) for w in work)}</ul>
  </div>
</section>

{cta_block()}"""
    page("/work/", "Work", "Websites Quincy Lou has designed, built and optimised, with the numbers behind each one.", body)


def build_case_studies() -> None:
    work = C["work"]
    for i, w in enumerate(work):
        nxt = work[(i + 1) % len(work)]
        sector = sector_of(w)
        stats = "".join(f'<li class="l-card"><p class="l-num">{e(v)}</p><p class="l-card__cap">{e(k)}</p></li>' for v, k in w["stats"])
        meta = "".join(f'<div><span>{e(k)}</span><b>{e(v)}</b></div>'
                       for k, v in [("Service", w["service"]), ("Industry", w["industry"]), ("Year", w["year"]), ("Result", w["result"])])
        head = doc_head(f'<span class="l-pill l-pill--mint">{e(sector)}</span>', w["name"], w["line"],
                        ph(f"{w['name']} website on a laptop", "") + f'<span class="l-pill l-pill--mint">{e(w["result"])}</span>', meta)
        body = f"""<section class="l-section l-section--first">
  <div class="l-wrap l-doc">
    <a class="l-back" href="/work/">{icon('left')}All case studies</a>
    {head}
    <ul class="l-stats">{stats}</ul>
    <div class="l-card l-parts">
      <div><h2>The problem</h2><p>{e(w['challenge'])}</p></div>
      <div><h2>What we did</h2><p>{e(w['approach'])}</p></div>
      <div><h2>What changed</h2><p>{e(w['outcome'])}</p></div>
    </div>
  </div>
  <div class="l-wrap l-gallery">
    <div class="l-gallery__wide">{ph(f"{w['name']} homepage on desktop", '')}</div>
    <div>{ph(f"{w['name']} on a phone", '')}</div>
    <div>{ph(f"{w['name']} detail", '')}</div>
  </div>
  <div class="l-wrap l-doc">
    <figure class="l-quote">
      <blockquote>{e(w['quote'])}</blockquote>
      <figcaption>{ph('Client photo', 'l-voice__photo')}<div><b>[Client name]</b><span>[Role], {e(w['name'])}</span></div></figcaption>
    </figure>
    <a class="l-next" href="/work/{e(nxt['slug'])}/"><div><span>Next case study</span><b>{e(nxt['name'])}</b><em>{e(nxt['line'])}</em></div><span class="l-next__arrow">{icon('right')}</span></a>
  </div>
</section>

{cta_block()}"""
        page(f"/work/{w['slug']}/", w["name"], f"{w['name']}: {w['line']}. {w['result']}.", body)


def build_studio() -> None:
    st = C["studio"]
    ways = "".join(f"""<li class="l-card l-problem"><span class="l-pill l-pill--mint">0{i + 1}</span><h3>{e(w['title'])}</h3><p>{e(w['text'])}</p></li>"""
                   for i, w in enumerate(st["ways"]))
    team = "".join(f"""<li class="l-member">{ph(f"Portrait of {m['name']}", '')}<div><h3>{e(m['name'])}</h3><p>{e(m['role'])}</p><p class="l-member__line">{e(m['line'])}</p></div></li>"""
                   for m in C["team"])
    beliefs = "".join(f'<li><span class="l-yes">{icon("check")}</span>{e(x)}</li>' for x in st["beliefs"])
    hire = st["hiring"]
    body = f"""<section class="l-section l-section--first" aria-labelledby="page-h">
  <div class="l-wrap">
    {list_head('Studio', ' '.join(st['title']), st['lede'])}
    <div class="l-studio-shot">{ph('The team in the studio', '')}<span class="l-pill">{e(st['place'])}</span></div>
    <ul class="l-problems l-problems--three">{ways}</ul>
  </div>
</section>

<section class="l-section" aria-labelledby="team-h">
  <div class="l-wrap">
    <div class="l-head l-head--center"><span class="l-pill">The team</span><h2 id="team-h">{e(' '.join(C['home']['team_title']))}</h2><p>{e(C['home']['team_lede'])}</p></div>
    <ul class="l-team">{team}</ul>
  </div>
</section>

<section class="l-section" aria-labelledby="beliefs-h">
  <div class="l-wrap">
    <div class="l-head l-head--center"><span class="l-pill">Principles</span><h2 id="beliefs-h">{e(st['beliefs_label'])}.</h2></div>
    <ul class="l-card l-beliefs">{beliefs}</ul>
    <div class="l-card l-hiring">
      <div><h3>{e(hire['title'])}</h3><p>{e(hire['text'])}</p></div>
      <a class="l-btn l-btn--dark" href="mailto:{e(S['email'])}">{e(hire['cta'])}</a>
    </div>
  </div>
</section>

{cta_block()}"""
    page("/studio/", "Studio", "Quincy Lou is a small website studio for service businesses. Four people, no middlemen.", body)


def build_journal() -> None:
    posts = sorted(C["journal"], key=lambda p: p["date"], reverse=True)
    f, rest = posts[0], posts[1:]
    body = f"""<section class="l-section l-section--first" aria-labelledby="page-h">
  <div class="l-wrap">
    {list_head('Journal', 'Notes on websites that bring in work.', 'Short, practical pieces for owners of dental practices, trades and construction firms.')}
    <a class="l-feature is-large l-feature--link" href="/journal/{e(f['slug'])}/">
      <div class="l-visual l-case__img--blue">{ph(f"Cover image for {f['title']}", '')}<span class="l-pill l-pill--mint">{nice_date(f['date'])}</span></div>
      <div class="l-feature__content is-large">
        <span class="l-pill l-pill--grey">{e(f['tag'])}</span>
        <h2>{e(f['title'])}</h2><p>{e(f['lede'])}</p>
        <span class="l-case__more">Read the article{icon('right')}</span>
      </div>
    </a>
    <ul class="l-cases l-cases--two">{''.join(post_card(p) for p in rest)}</ul>
  </div>
</section>

{cta_block()}"""
    page("/journal/", "Journal", "Practical notes on websites for service businesses, from the Quincy Lou studio.", body)


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
        more = "".join(post_card(q) for q in [q for q in posts if q["slug"] != p["slug"]][:3])
        meta = (f'<div class="l-doc__author"><span class="l-logo__mark l-doc__avatar">{icon("mark")}</span><div><b>{e(S["name"])} studio</b><span>{e(p["read"])} read</span></div></div>'
                '<a class="l-btn l-btn--dark" href="#review">Get a free review</a>')
        head = doc_head(f'<span class="l-pill l-pill--mint">{e(p["tag"])}</span>', p["title"], p["lede"],
                        ph(f"Cover image for {p['title']}", "") + f'<span class="l-pill l-pill--mint">{nice_date(p["date"])}</span>', meta)
        body = f"""<section class="l-section l-section--first">
  <div class="l-wrap l-doc">
    <a class="l-back" href="/journal/">{icon('left')}All articles</a>
    <article class="l-doc__article">
      {head}
      <div class="l-card l-prose">{''.join(blocks)}</div>
    </article>
  </div>
</section>

<section class="l-section" aria-labelledby="more-h">
  <div class="l-wrap">
    <div class="l-head l-head--split"><div><span class="l-pill">Journal</span><h2 id="more-h">Keep reading.</h2></div><a class="l-btn l-btn--dark" href="/journal/">All articles</a></div>
    <ul class="l-cases">{more}</ul>
  </div>
</section>

{cta_block()}"""
        page(f"/journal/{p['slug']}/", p["title"], p["lede"], body)


def build_contact() -> None:
    ct = C["contact"]
    h = C["home"]
    faq = "".join(f"""<details class="l-qa"{' open' if i == 0 else ''}><summary>{e(q)}<i aria-hidden="true"></i></summary><p>{e(a)}</p></details>"""
                  for i, (q, a) in enumerate(ct["faq"]))
    addr = "<br>".join(e(x) for x in S["address"])
    body = f"""<section class="l-section l-section--first" id="review" aria-labelledby="page-h">
  <div class="l-wrap">
    {list_head('Contact', ' '.join(h['form_title']), h['form_lede'])}
    <div class="l-contact">
      {review_form('contact')}
      <aside class="l-card l-info" aria-label="Contact details">
        <h2>Talk to a person</h2>
        <dl>
          <div><dt>Phone</dt><dd><a href="tel:{S['phone_href']}">{e(S['phone'])}</a></dd></div>
          <div><dt>Email</dt><dd><a href="mailto:{e(S['email'])}">{e(S['email'])}</a></dd></div>
          <div><dt>Studio</dt><dd>{addr}</dd></div>
          <div><dt>Hours</dt><dd>{e(S['hours'])}</dd></div>
        </dl>
        <p class="l-info__note"><span class="l-yes">{icon('check')}</span>{e(S['reply_time'])}.</p>
      </aside>
    </div>
  </div>
</section>

<section class="l-section" id="faq" aria-labelledby="faq-h">
  <div class="l-wrap l-faq">
    <div class="l-faq__head">
      <span class="l-pill">FAQ</span>
      <h2 id="faq-h">{e(' '.join(ct['faq_title']))}</h2>
      <p>{e(ct['faq_lede'])}</p>
    </div>
    <div class="l-qas">{faq}</div>
  </div>
</section>"""
    page("/contact/", "Contact", "Get in touch with Quincy Lou for a free website review. We reply within one working day.", body)


def build_privacy() -> None:
    pv = C["privacy"]
    secs = "".join(f"<h2>{e(h)}</h2><p>{e(t)}</p>" for h, t in pv["sections"])
    body = f"""<section class="l-section l-section--first l-section--last">
  <div class="l-wrap l-doc">
    {doc_head('<span class="l-pill l-pill--mint">Legal</span>', 'Privacy policy', f"Last updated {pv['updated']}. Plain English, as short as we could make it.")}
    <div class="l-card l-prose">{secs}<h2>Contact</h2><p>Questions about this policy: <a href="mailto:{e(S['email'])}">{e(S['email'])}</a>. {e(S['company'])}</p></div>
  </div>
</section>"""
    page("/privacy/", "Privacy", "How Quincy Lou collects and uses personal information.", body, review=False)


def simple_page(path: str, title: str, desc: str, tag: str, heading: str, text: str, buttons: str) -> None:
    body = f"""<section class="l-section l-section--first l-section--last">
  <div class="l-wrap l-doc">
    <div class="l-card l-notice">
      <span class="l-pill l-pill--mint">{e(tag)}</span>
      <h1>{e(heading)}</h1>
      <p>{e(text)}</p>
      <div class="l-hero__buttons">{buttons}</div>
    </div>
  </div>
</section>"""
    page(path, title, desc, body, review=False)


def build_thanks() -> None:
    simple_page("/thanks/", "Thank you", "Thanks for getting in touch with Quincy Lou.", "Message sent", "Thank you.",
                f"Your message is with us. {S['reply_time']}, usually much sooner.",
                f'<a class="l-btn l-btn--dark" href="/">Back to the homepage</a><a class="l-btn l-btn--line" href="/work/">See our work</a>')


def build_404() -> None:
    simple_page("/404", "Page not found", "This page could not be found.", "Error 404", "Page not found.",
                "That link has moved or never existed. The useful parts of the site are one click away.",
                f'<a class="l-btn l-btn--dark" href="/">Go to the homepage</a><a class="l-btn l-btn--line" href="/work/">See our work</a>')


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
