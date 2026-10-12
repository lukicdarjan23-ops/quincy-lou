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
        "star4": '<path d="M8 2v12M2 8h12M3.8 3.8l8.4 8.4M12.2 3.8l-8.4 8.4" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>',
        "pen": '<path d="M4 20 5.5 14 15 4.5l4.5 4.5L10 18.5zM13 6.5 17.5 11" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
        "cursor": '<path d="m5 4 13 5.5-5.6 1.9-1.9 5.6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M3 15.5l2-1M15 20l-.6-2.2M20 13.5l-2.1-.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
        "chart": '<path d="M4 20V10m6 10V4m6 16v-7m4 7H2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
        "search": '<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m15.5 15.5 5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
        "next": '<path d="M5 24h38M30 11l13 13-13 13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
        "quote": '<path d="M0 40V24C0 10 7 2 20 0l2 6c-7 2-11 7-11 14h9v20zm30 0V24C30 10 37 2 50 0l2 6c-7 2-11 7-11 14h9v20z" fill="currentColor"/>',
    }
    vb = {"pen": "0 0 24 24", "cursor": "0 0 24 24", "chart": "0 0 24 24", "search": "0 0 24 24",
          "next": "0 0 48 48", "quote": "0 0 52 40"}.get(name, "0 0 16 16")
    return f'<svg{c} viewBox="{vb}" aria-hidden="true">{paths[name]}</svg>'


def btn(label: str, href: str, kind: str = "red", size: str = "", arrow: bool = True, extra: str = "") -> str:
    cls = f"btn btn--{kind}" + (f" btn--{size}" if size else "") + (f" {extra}" if extra else "")
    a = icon("arrow", "arr") if arrow else ""
    return f'<a class="{cls}" href="{e(href)}">{e(label)}{a}</a>'


def acc_title(parts: list[str], tag: str = "h2", attrs: str = "") -> str:
    """Two-part headline: the first part in the grotesk, the second as the italic accent."""
    first, second = parts
    return f'<{tag}{attrs}>{e(first)}<br><span class="acc">{e(second)}</span></{tag}>'


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
    <a class="logo" href="/" aria-label="{e(S['name'])}, home">{e(S['name'].lower())}<i aria-hidden="true"></i></a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <div class="hdr__right">
      <span class="avail"><i aria-hidden="true"></i>{e(S['availability'])}</span>
      <a class="hdr__phone" href="tel:{S['phone_href']}">{e(S['phone'])}</a>
      {btn(S['cta'], '/contact/', 'ink', 'sm')}
      <details class="menu">
        <summary>Menu</summary>
        <nav class="menu__panel" aria-label="Mobile">{mlinks}<a href="/contact/">Contact</a>
          <a class="btn btn--red" href="tel:{S['phone_href']}">Call {e(S['phone'])}</a>
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
  <button class="btn btn--ink btn--block btn--lg" type="submit">Send and get my review{icon('arrow', 'arr')}</button>
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
      {btn('Get a free website review', '/contact/', 'cream-on-ink')}
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
        <button class="btn btn--red btn--sm" type="submit">Join</button>
      </form>
    </div>
  </div>
  <span class="wordmark" aria-hidden="true">{e(S['name'].lower())}</span>
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
ACCENTS = ["lime", "lavender", "coral", "mint", "pink"]


def work_card(w: dict, ratio: str) -> str:
    tone = w.get("badge") or ACCENTS[[x["slug"] for x in C["work"]].index(w["slug"]) % len(ACCENTS)]
    return f"""<a class="card-work" href="/work/{e(w['slug'])}/" data-r>
  <div class="card-work__media">
    <span class="badge badge--{tone}">{icon('arrow')}{e(w['result'])}</span>
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


def receipts_block() -> str:
    """The proof section: a short pitch beside a stats card styled as a till receipt."""
    r = C["home"]["receipts"]
    lines = "".join(f'<li><span>{e(k)}</span><i aria-hidden="true"></i><b>{e(v)}</b></li>' for k, v in r["lines"])
    tools = "".join(f'<li class="tool">{e(t)}</li>' for t in r["tools"])
    return f"""<section class="band receipts-band" aria-labelledby="rcpt-h">
  <div class="wrap">
    <div class="receipts">
      <div class="receipts__copy">
        {acc_title(r['title'], 'h2', ' id="rcpt-h" data-r')}
        <p data-r="100">{e(r['lede'])}</p>
      </div>
      <div class="receipt-wrap" data-r="120"><figure class="receipt" aria-label="Studio numbers">
        <p class="receipt__store">{e(r['store'])}</p>
        <p class="receipt__sub">{e(r['sub'])}</p>
        <ul class="receipt__lines">{lines}</ul>
        <p class="receipt__total"><span>{e(r['total'][0])}</span><b>{e(r['total'][1])}</b></p>
        <span class="receipt__barcode" aria-hidden="true"></span>
        <p class="receipt__note">{e(r['note'])}</p>
      </figure></div>
    </div>
    <div class="tools" data-r>
      <div class="tools__head"><h3>{e(r['tools_title'])}</h3><p>{e(r['tools_lede'])}</p></div>
      <ul class="tools__list">{tools}</ul>
    </div>
  </div>
</section>"""


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


def enquire_block() -> str:
    h = C["home"]
    return f"""<section class="band" id="enquire" aria-labelledby="enq-h">
  <div class="wrap">
    <div class="enquire" data-r>
      <div>
        {acc_title(h['form_title'], 'h2', ' id="enq-h"')}
        <p class="enquire__lede">{e(h['form_lede'])}</p>
        <div class="enquire__alt">
          <a href="mailto:{e(S['email'])}">Prefer email? {e(S['email'])}</a>
          <a href="tel:{S['phone_href']}">Or ring {e(S['phone'])}</a>
          <span>{e(S['reply_time'])}.</span>
        </div>
      </div>
      {enquiry_form()}
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------- pages
def build_home() -> None:
    h = C["home"]
    names = "".join(f'<span class="marquee__name">{e(n)}</span><span class="marquee__dot" aria-hidden="true"></span>'
                    for n in h["clients"])
    services = "".join(f"""<a class="svc svc--{s['tone']}" href="{e(s.get('link', '/contact/'))}">
  <div class="svc__copy">
    {icon(s['icon'], 'svc__icon')}
    <h3>{e(s['name'])}</h3>
    <p>{e(s['text'])}</p>
    <p class="svc__price"><b>{e(s['price'])}</b><span>· {e(s['time'])}</span></p>
  </div>
  <div class="svc__media">{ph(f"{s['name']} example image", "", "")}</div>
</a>""" for s in C["services"])
    steps = "".join(f"""<li class="step step--{p['tone']}" data-r="{i * 90}">
  <span class="step__tape" aria-hidden="true"></span>
  <div class="step__top"><span class="step__n">{e(p['n'])}</span><span class="step__when">{e(p['when'])}</span></div>
  <h3>{e(p['title'])}</h3><p>{e(p['text'])}</p>
</li>""" for i, p in enumerate(C["process"]))
    plans = ""
    for i, p in enumerate(C["pricing"]):
        hot = p.get("featured")
        items = "".join(f"<li>{icon('check')}<span>{e(it)}</span></li>" for it in p["items"])
        badge = f'<span class="plan__badge">{e(p["badge"])}</span>' if p.get("badge") else ""
        plans += f"""<article class="plan{' plan--hot' if hot else ''}" data-r="{i * 90}">
  <div class="plan__top"><h3>{e(p['name'])}</h3>{badge}</div>
  <p class="plan__price"><b>{e(p['price'])}</b><span>{e(p['unit'])}</span></p>
  <p class="plan__text">{e(p['text'])}</p>
  <ul>{items}</ul>
  {btn(p['cta'], '/contact/', 'ink' if hot else 'line')}
</article>"""
    t = C["testimonials"]
    others = "".join(f"""<figure class="voice" data-r="{i * 80}">
  <span class="stars" aria-label="5 out of 5">★★★★★</span>
  <blockquote>{e(v['quote'])}</blockquote>
  <figcaption class="who">{ph('Client photo', 'ph--avatar')}<span><b>{e(v['name'])}</b><span>{e(v['role'])}</span></span></figcaption>
</figure>""" for i, v in enumerate(t["others"]))
    posts = "".join(post_card(p, i) for i, p in enumerate(C["journal"][:3]))
    f = t["featured"]

    body = f"""
<section class="hero">
  <div class="wrap">
    <h1 data-r>Websites <span class="inline-ph" role="img" aria-label="Photo of a finished client website"></span> that make the
      <span class="inline-mark" aria-hidden="true">{icon('star4')}</span> <span class="acc">phone</span> ring
      more often. <span class="inline-ph inline-ph--2" role="img" aria-label="Photo of the team at work"></span></h1>
    <div class="hero__foot">
      <div data-r="120">
        <p class="hero__lede">{e(h['hero_lede'])}</p>
        <div class="hero__ctas">{btn(S['cta'], '/contact/', 'red', 'lg')}{btn('See our work', '/work/', 'line', 'lg')}</div>
      </div>
      <div class="rating" data-r="200">
        <div class="avatars">{ph('Client', 'ph--avatar')}{ph('Client', 'ph--avatar')}{ph('Client', 'ph--avatar')}{ph('Client', 'ph--avatar')}</div>
        <div class="rating__txt"><span class="stars" aria-hidden="true">★★★★★</span>{e(S['rating'])}</div>
      </div>
    </div>
  </div>
</section>

<section class="clients" aria-label="Clients">
  <p>{e(h['clients_label'])}</p>
  <div class="marquee"><div class="marquee__track">
    <div class="marquee__set">{names}</div><div class="marquee__set" aria-hidden="true">{names}</div>
  </div></div>
</section>

<section class="band" id="work" aria-labelledby="work-h" style="padding-top:clamp(32px,3.4vw,48px)">
  <div class="wrap">
    <div class="head">{acc_title(h['work_title'], 'h2', ' id="work-h" data-r')}
      <div class="head__side" data-r="120"><p>{e(h['work_lede'])}</p>{btn('All projects', '/work/', 'line', 'sm')}</div></div>
    {work_grid(C['work'][:4])}
  </div>
</section>

{receipts_block()}

<section class="band" id="services" aria-labelledby="svc-h">
  <div class="wrap">
    <div class="head">{acc_title(h['services_title'], 'h2', ' id="svc-h" data-r')}
      <div class="head__side" data-r="120"><p>{e(h['services_lede'])}</p></div></div>
    <div class="svc-stack">{services}</div>
  </div>
</section>

<section class="band" id="process" aria-labelledby="proc-h" style="padding-top:0">
  <div class="wrap">
    <div class="head head--line"><h2 id="proc-h" data-r>{e(h['process_title'][0])} <span class="acc">{e(h['process_title'][1])}</span></h2></div>
    <ol class="process">{steps}</ol>
  </div>
</section>

<section class="band" id="pricing" aria-labelledby="price-h" style="padding-top:0">
  <div class="wrap">
    <div class="head">{acc_title(h['pricing_title'], 'h2', ' id="price-h" data-r')}
      <div class="head__side" data-r="120"><p>Fixed prices for projects, one monthly price for ongoing work. Every quote is in writing before anything starts.</p></div></div>
    <div class="plans">{plans}</div>
    <p class="plans__note">{icon('spark')}<span>{e(h['pricing_note'])}</span></p>
  </div>
</section>

<section class="band dark" aria-labelledby="voices-h">
  <div class="wrap">
    <div class="head">{acc_title(h['voices_title'], 'h2', ' id="voices-h" data-r')}
      <div class="head__side" data-r="120"><p>Unedited, from the people who pay the invoices.</p></div></div>
    <div class="voices">
      <figure class="voice-hero" data-r>
        {icon('quote')}
        <blockquote>{e(f['quote'])}</blockquote>
        <figcaption class="who">{ph('Client photo', 'ph--avatar')}<span><b>{e(f['name'])}</b><span>{e(f['role'])}</span></span></figcaption>
      </figure>
      <div class="voice-grid">{others}</div>
    </div>
  </div>
</section>

<section class="band team-band" aria-labelledby="team-h">
  <div class="wrap">
    <div class="head head--line"><h2 id="team-h" data-r>{e(h['team_title'][0])} <span class="acc">{e(h['team_title'][1])}</span></h2>
      <div class="head__side" data-r="120"><p>{e(h['team_lede'])}</p></div></div>
    {team_block()}
  </div>
</section>

<section class="band notes-band" aria-labelledby="notes-h">
  <div class="wrap">
    <div class="head head--line"><h2 id="notes-h" data-r>{e(h['journal_title'][0])} <span class="acc">{e(h['journal_title'][1])}</span></h2>
      {btn('Read the journal', '/journal/', 'line', 'sm')}</div>
    <div class="posts">{posts}</div>
  </div>
</section>

{enquire_block()}
"""
    page("/", S["name"], S["description"], body)


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
{enquire_block()}
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
    nums = "".join(f'<div data-r="{i * 80}"><b>{e(v)}</b><span>{e(k)}</span></div>' for i, (v, k) in enumerate(st["numbers"]))
    story = "".join(f"<p>{e(p)}</p>" for p in st["story"])
    values = "".join(f"""<div class="value" data-r="{i * 80}"><span>0{i + 1}</span><h3>{e(v['title'])}</h3><p>{e(v['text'])}</p></div>"""
                     for i, v in enumerate(st["values"]))
    body = f"""
<section class="page-hero">
  <div class="wrap page-hero__row">
    {acc_title(st['title'], 'h1', ' data-r')}
    <p class="page-hero__side" data-r="120">{e(st['lede'])}</p>
  </div>
</section>
<section><div class="wrap" data-r>{ph('The team in the studio', 'ph--reel')}</div></section>
<section class="band">
  <div class="wrap story">
    <div data-r>{story}</div>
    <div data-r="120">{ph('A client project in progress', 'ph--r43')}</div>
  </div>
</section>
<section class="band" style="padding-top:0"><div class="wrap numbers">{nums}</div></section>
<section class="band" style="padding-top:0">
  <div class="wrap">
    <div class="head">{acc_title(st['values_title'], 'h2', ' data-r')}</div>
    <div class="values">{values}</div>
  </div>
</section>
<section class="band" style="padding-top:0">
  <div class="wrap">
    <div class="head head--line"><h2 data-r>{e(C['home']['team_title'][0])} <span class="acc">{e(C['home']['team_title'][1])}</span></h2>
      <div class="head__side" data-r="120"><p>{e(C['home']['team_lede'])}</p></div></div>
    {team_block()}
  </div>
</section>
{enquire_block()}
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
        <div class="post__meta"><span class="chip-ink">{e(f['tag'])}</span><span>{nice_date(f['date'])} · {e(f['read'])}</span></div>
        <h2>{e(f['title'])}</h2>
        <p>{e(f['lede'])}</p>
        <span class="btn btn--line btn--sm">Read the article{icon('arrow', 'arr')}</span>
      </div>
    </a>
    <div class="posts">{grid}</div>
  </div>
</section>
{enquire_block()}
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
    <div class="head"><h2>Keep <span class="acc">reading.</span></h2>{btn('All articles', '/journal/', 'line', 'sm')}</div>
    <div class="posts">{more}</div>
  </div>
</section>
"""
        page(f"/journal/{p['slug']}/", p["title"], p["lede"], body, "Journal")


def build_contact() -> None:
    ct = C["contact"]
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in ct["faq"])
    addr = "<br>".join(e(x) for x in S["address"])
    body = f"""
<section class="page-hero">
  <div class="wrap page-hero__row">
    {acc_title(ct['title'], 'h1', ' data-r')}
    <p class="page-hero__side" data-r="120">{e(ct['lede'])}</p>
  </div>
</section>
<section class="band" style="padding-top:0">
  <div class="wrap contact-grid">
    <div data-r>{enquiry_form('contact')}</div>
    <div class="contact-side">
      <div class="card" data-r="80">
        <h3>Talk to a person</h3>
        <dl>
          <div><dt>Phone</dt><dd><a href="tel:{S['phone_href']}">{e(S['phone'])}</a></dd></div>
          <div><dt>Email</dt><dd><a href="mailto:{e(S['email'])}">{e(S['email'])}</a></dd></div>
          <div><dt>Studio</dt><dd>{addr}</dd></div>
          <div><dt>Hours</dt><dd>{e(S['hours'])}</dd></div>
        </dl>
      </div>
      <div class="card card--ink faq" data-r="160"><h3>Before you ask</h3>{faq}</div>
    </div>
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
  <div class="hero__ctas">{btn('Back to the homepage', '/', 'red')}{btn('Read the journal', '/journal/', 'line')}</div>
</div></section>
"""
    page("/thanks/", "Thank you", "Thanks for getting in touch with Quincy Lou.", body)


def build_404() -> None:
    body = f"""
<section class="page-hero"><div class="wrap lost">
  <h1>Page<br><span class="acc">not found.</span></h1>
  <p class="hero__lede">That link has moved or never existed. The useful parts of the site are one click away.</p>
  <div class="hero__ctas">{btn('Go to the homepage', '/', 'red')}{btn('See our work', '/work/', 'line')}</div>
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
