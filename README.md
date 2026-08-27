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

**Colour.** `--ink #101014` · `--ground #F2F1EE` (a warm-biased neutral, not a flat
grey) · `--paper #FFFFFF` · `--violet #6A4DFF` · `--lilac #EBE6FF` ·
`--melon #FF7A59` · `--pitch #131317`. Violet carries every call to action; melon
appears only on figures and the headline underline. Everything else stays quiet.

**Type.** Schibsted Grotesk at 800/900 with tight negative tracking for display,
Instrument Sans at 400/500 for body. Both from Google Fonts, with real fallback
stacks.

**Layout.** A 1120px column, alternating ground/paper bands, 28px card radii and
pill CTAs.

**Theming.** Light and dark are both designed. All colour lives in tokens defined
on bare `:root`, redefined under `@media (prefers-color-scheme: dark)` (guarded as
`:root:not([data-theme="light"])`) and again under `:root[data-theme="dark"]`, so
the page resolves correctly whether the viewer set a theme explicitly or left it on
system. No component sets a colour outside the token set.

**Accessibility.** Every sampled text/background pair clears WCAG AA in both
themes. Visible 3px focus rings, a skip link, keyboard-operable FAQ, and
`prefers-reduced-motion` disables the reveal animation entirely rather than
speeding it up.

## Images

Every image is an intentionally blank rectangle (`.plate`). No placeholder
photography or generated imagery is used anywhere. Swap the `<span class="plate">`
elements for real `<img>` tags, keeping the `aria-label` text as `alt`.

## Placeholder content

Quincy Lou is not a real company. The phone number is in Ofcom's reserved
drama range, and the address, company number, team names, client names, case
study figures and review counts are all invented for the layout. Replace them
before this goes anywhere near production.
