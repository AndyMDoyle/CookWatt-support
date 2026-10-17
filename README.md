# CookWatt support

Public support and privacy pages for CookWatt, hosted with GitHub Pages.
The app's source code is not included in this repository.

## App Store Connect URLs

- **Support:** https://andymdoyle.github.io/CookWatt-support/
- **Privacy policy:** https://andymdoyle.github.io/CookWatt-support/privacy.html
- **Contact:** apps@andydoyle.org

Both pages follow the app's cream/terracotta and warm-charcoal/peach palettes,
automatically choosing light or dark mode from the visitor's system appearance.
The site uses no JavaScript, analytics, remote fonts, or contact forms.

## Local preview

From this directory:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000/. No dependency installation or build step is needed.

## Checks

```sh
python3 -m unittest discover -s tests
```

## Publishing

GitHub Pages is configured to deploy from the root of the `main` branch.
Commit and push changes to publish them. `.nojekyll` keeps the site a plain
static deployment.

Keep the privacy policy aligned with the app's actual data handling, including
any future analytics, cloud services, or new SDKs. Update its date when the
policy changes. The policy also distinguishes optional support correspondence,
GitHub's website hosting, and Apple's platform services from the app's local
calculations.

The app's Settings pane should link to the privacy policy; that integration is
separate from this website.

## Files

- `index.html`: support, usage instructions, FAQ, and email contact.
- `privacy.html`: publicly accessible privacy policy.
- `styles.css`: shared responsive light/dark styling.
- `assets/`: resized, sRGB versions of CookWatt's original light/dark icons.
- `tests/`: dependency-free checks for page metadata, links, contact details,
  navigation, and local-only assets.

Copyright © 2026 Andy Doyle.
