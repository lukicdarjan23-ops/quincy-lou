# Quincy Lou

A conversion-focused marketing site for a fictional web design studio, built as a
static site with no build step. Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

## Pages

| File | What it is |
| --- | --- |
| `index.html` | Homepage |
| `services/design.html` | Design service page |
| `services/build.html` | Build service page |
| `services/optimise.html` | Optimise service page |
| `assets/css/site.css` | The whole design system |
| `assets/js/site.js` | Scroll reveal, and nothing else |

## Homepage structure

Each section maps to a specific job:

1. **Header** — logo top left with a one-line description of the business directly
   under it, so the upper-left corner orients a first-time visitor. Phone number
   top right, at 20px, not buried in the footer.
2. **Hero** — headline is about the visitor's outcome (booked jobs), not our craft.
   Primary CTA "Get a website review" for people ready to act, secondary
   "Explore our work" for people still browsing.
3. **Trust bar** — sits directly under the hero CTAs: client logos, review score,
   years in business, sites shipped. Repeated at the closing CTA, because trust
   belongs next to every place we ask someone to act.
4. **The problem** — three sentences naming what is broken, plus four symptom
   cards, so the visitor sees themselves before they see us.
5. **What we do** — design, build, optimise. Each block links to its own page.
6. **Featured results** — three case studies, each led by a number rather than a
   screenshot.
7. **Process** — four steps with a duration on each, to remove the fear of the
   unknown.
8. **Testimonials** — deliberately three different formats (video, written,
   review-platform screenshot). Repeating one trust symbol causes trust blindness.
9. **Objection handling** — price, timeline, "we already have a designer", and
   "we tried this before".
10. **Price anchor** — a starting-from number with an explicit what's-in /
    what's-not split.
11. **FAQ** — seven questions, native `<details>` so it works without JavaScript.
12. **Closing CTA** — its own trust bar, and a reassurance line beside the button.
13. **Footer** — phone, email, physical address, and the people you would deal with.

## Design system

Modelled on designjoy.co's visual language.

**Colour.** `--ground #EFEEEA` (warm light grey) · `--paper #FFFFFF` ·
`--ink #0D0D0D` · `--ash #5C5C56` · `--ash-light #6A6A64`. There is deliberately
no flat brand hue. All colour arrives through **gradient blobs** (`.blob-1`
through `.blob-5` and `.blob-full`), each built from four or five layered
`radial-gradient()` stops so they read as soft multi-colour fields rather than
linear ramps. One full-black band carries the pricing card, the closing CTA and
the footer.

**Type.** The signature is a bold grotesk mixed with an italic serif *inside the
same headline*: Schibsted Grotesk 800 with -0.042em tracking for the sans,
Instrument Serif Italic for the emphasised words ("done *properly*",
"*Frequently* asked questions"). Instrument Sans carries body copy. Any `<em>`
inside a heading picks up the serif automatically.

**Layout.** A 1080px column. Left-aligned hero with a gradient card alongside,
centred section heads, white cards at 22px radius with no shadow, black pill
CTAs, and tiny uppercase letterspaced eyebrows rather than coloured pills.

**Theming.** This is a committed single-look light design, matching the brand it
is modelled on. There is no dark variant, so every colour — including `body`
background — is painted explicitly from tokens rather than inherited, and the
page holds on any host ground.

**Accessibility.** All 29 sampled text/background pairs clear WCAG AA. Visible
focus rings, a skip link, keyboard-operable FAQ via native `<details>`, and
`prefers-reduced-motion` disables the reveal animation entirely.

## Images

Every image is an intentionally blank rectangle (`.plate`). No placeholder
photography or generated imagery is used anywhere. Swap the `<span class="plate">`
elements for real `<img>` tags, keeping the `aria-label` text as `alt`.

## Placeholder content

Quincy Lou is not a real company. The phone number is in Ofcom's reserved
drama range, and the address, company number, team names, client names, case
study figures and review counts are all invented for the layout. Replace them
before this goes anywhere near production.
