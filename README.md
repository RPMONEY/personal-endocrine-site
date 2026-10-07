# Personal Endocrine website

Static site for Personal Endocrine, P.C. (Jinsun Choi, MD), North Tustin, CA.
Hosted on Cloudflare Workers (static assets).

## Folders

| Folder | What it is |
|---|---|
| `site/` | The finished website. This is what Cloudflare serves. |
| `source-pages/` | Design canvas pages (`*.dc.html`) the site is built from. |
| `tools/` | Build and edit scripts. `build.py` turns `source-pages/` into `site/`. |
| `img/` | Photos used on the site. |
| `logos/` | Logo files (SVG, PNG, PDF). |

## Rebuild the site

```
python3 tools/build.py source-pages img/dr-jinsun-choi.jpg site <BUILD_NUMBER>
```

The build number is stamped into `site/version.txt` and an HTML comment on every page,
so the live site shows which build it is (`/version.txt`).

## Deploy

`wrangler.jsonc` tells Cloudflare to serve `site/`. Once this repo is connected to the
Cloudflare Worker, every push to `main` deploys automatically.

## Open items before launch

- Notice of Privacy Practices: Privacy Officer and privacy contact email
- Appointment and email signup forms have no backend yet (they tell visitors to call)
- Office hours (footer line removed until confirmed)
- Redirects from any old site URLs beyond those in `_redirects`
