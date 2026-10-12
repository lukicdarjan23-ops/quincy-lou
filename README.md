# Quincy Lou

Website for Quincy Lou, a studio that designs, builds and optimises websites
for service businesses. Plain static HTML and CSS, hosted on Netlify.

## Where things are

| Path | What it is |
| --- | --- |
| `content/site.json` | **All the words, projects, prices, team and articles.** Edit this. |
| `tools/build.py` | Turns `content/site.json` into the HTML pages in `site/` |
| `site/` | The published website (Netlify serves this folder) |
| `site/assets/css/main.css` | The whole design: colours, type, layout |
| `site/assets/js/main.js` | Scroll reveal and mobile menu. The site works without it |
| `site/concept/` | Earlier design directions, kept for reference and hidden from search |
| `netlify.toml` | Netlify settings: publish `site/`, security headers |

## Pages

Home · Work · 8 case studies · Studio · Journal · 5 articles · Contact ·
Privacy · Thank-you page (after a form is sent) · 404

## Changing content

1. Edit `content/site.json`
2. Run `python3 tools/build.py` (standard Python 3, nothing to install)
3. Commit and push. Netlify publishes the new version automatically

To add a client project, copy one of the objects in `"work"`, give it a new
`slug` and fill it in. The build creates its page and adds it to the Work grid
and the sitemap. Articles in `"journal"` work the same way.

## What is still a placeholder

- **Every image** is a blank shape. Swap a `<span class="ph …">` for an `<img>`
  (or add an `image` field in the content and the template).
- **Clients, team, testimonials and project results** are named
  `Client 0X`, `Name Surname`, `Client name` or written in `[square brackets]`.
  Replace them with real ones before launch. Do not publish the sample numbers
  as your own results.
- The phone number is in Ofcom's reserved drama range, and the address and
  company number are invented.

## Forms

The review form, contact form and newsletter use **Netlify Forms**. Nothing to
configure: Netlify detects them on the first deploy and submissions appear
under *Forms* in the Netlify dashboard, where you can turn on email
notifications.

## Deploying on Netlify

*Add new site → Import an existing project → GitHub →* this repo. Leave the
build command empty. `netlify.toml` already sets the publish folder to `site`.
