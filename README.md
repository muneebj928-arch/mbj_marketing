# Nook practice store

A free, fast, static e-commerce store. Product pages, cart, WhatsApp checkout, SEO files and tracking events are all included.

## 1. Change these first (data/store.json)

- `site_url`: your real address, for example https://mbj-marketing.github.io
- `whatsapp`: your number with country code and no plus sign, for example 923001234567
- `name`, `tagline`, and the products (name, price, description, features)

Then run `python build.py` (Python 3, nothing to install). It rebuilds every page, the sitemap and robots.txt.

## 2. Test on your computer

    python -m http.server 8000

Open http://localhost:8000

## 3. Deploy on GitHub Pages (free)

1. Create a public repo named exactly mbj-marketing.github.io
2. In this folder:

       git init
       git add .
       git commit -m "Launch store"
       git branch -M main
       git remote add origin https://github.com/mbj-marketing/mbj-marketing.github.io.git
       git push -u origin main

3. Repo Settings > Pages > Deploy from a branch > main > / (root) > Save
4. Your store is live in 1-3 minutes.

The store must live at the root of the domain (username.github.io, Netlify, or a custom domain).

## 4. Add products

Add a new item to `products` in data/store.json, put its image in images/, and run `python build.py`. Replace the SVG pictures with real product photos (JPG/WebP, under 150 KB each) when you have them.

## 5. After it is live (your marketing practice)

- Search Console: add the site, submit sitemap.xml
- Google Tag Manager: create a container, paste its ID into `gtm_id` in data/store.json, run `python build.py`, push. The store already sends view_item, add_to_cart, begin_checkout and purchase events to the dataLayer, so you can connect GA4 and the Meta Pixel in GTM.
- Create a Facebook page and Instagram account with the same brand name
- Build your Meta Ads draft campaign pointing to the home page
