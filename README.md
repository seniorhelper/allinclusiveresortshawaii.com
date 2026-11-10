# allinclusiveresortshawaii.com

Static guide site on GitHub Pages (custom domain in `CNAME`, verified to the seniorhelper account).

- Edit content in `_build/pages.py`, then run `python _build/build.py` to regenerate every page + `sitemap.xml`.
- `_build/make_images.py` regenerates the original graphics (og.jpg, logo.png).
- `_build/` is not published (Jekyll skips underscore folders). Don't add `.nojekyll`.
- No forms, no trackers, CSP via meta tag. Run the site-security-check scanner before every push.
