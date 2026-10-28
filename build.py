#!/usr/bin/env python3
"""
Builds the whole store from data/store.json.

Run:  python build.py
It writes: index.html, about.html, shipping-returns.html, checkout.html,
404.html, products/*.html, images/*.svg, sitemap.xml and robots.txt
"""
import json
import os
from html import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(ROOT, "data", "store.json"), encoding="utf-8"))
NAME = CFG["name"]
URL = CFG["site_url"].rstrip("/")
CUR = CFG["currency"]
PRODUCTS = CFG["products"]


def money(n):
    return f"{CUR} {n:,}"


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


# ------------------------------------------------------------------ images
def svg(bg, body):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" role="img">'
        f'<rect width="600" height="600" fill="{bg}"/>{body}</svg>'
    )


INK = "#16202A"


def make_images():
    imgs = {}
    p = {x["image"]: x["color"] for x in PRODUCTS}

    imgs["drawer-organizer.svg"] = svg(p["drawer-organizer.svg"], f"""
<rect x="60" y="190" width="480" height="260" rx="20" fill="#B98B52"/>
<rect x="80" y="210" width="130" height="220" rx="10" fill="#F5EAC8"/>
<rect x="225" y="210" width="150" height="100" rx="10" fill="#F5EAC8"/>
<rect x="225" y="330" width="150" height="100" rx="10" fill="#F5EAC8"/>
<rect x="390" y="210" width="130" height="100" rx="10" fill="#F5EAC8"/>
<rect x="390" y="330" width="130" height="100" rx="10" fill="#F5EAC8"/>
<rect x="105" y="150" width="14" height="190" rx="7" fill="{INK}"/>
<ellipse cx="112" cy="145" rx="22" ry="14" fill="{INK}"/>
<rect x="150" y="165" width="14" height="170" rx="7" fill="#0E6B66"/>
<ellipse cx="157" cy="160" rx="18" ry="12" fill="#0E6B66"/>""")

    tiers = ""
    for i, (y, w) in enumerate([(380, 400), (300, 330), (220, 260)]):
        x = 300 - w // 2
        tiers += f'<rect x="{x}" y="{y + 30}" width="{w}" height="22" rx="6" fill="{INK}"/>'
        n = w // 62
        for k in range(n):
            jx = x + 14 + k * 62
            col = ["#0E6B66", "#F2C94C", "#E07A5F", "#FFFFFF"][(k + i) % 4]
            tiers += f'<rect x="{jx}" y="{y - 14}" width="46" height="44" rx="6" fill="{col}"/>'
            tiers += f'<rect x="{jx + 4}" y="{y - 26}" width="38" height="14" rx="4" fill="{INK}"/>'
    imgs["spice-rack.svg"] = svg(p["spice-rack.svg"], tiers)

    imgs["shelf-riser.svg"] = svg(p["shelf-riser.svg"], f"""
<rect x="90" y="250" width="420" height="22" rx="6" fill="{INK}"/>
<rect x="115" y="272" width="16" height="170" fill="{INK}"/>
<rect x="469" y="272" width="16" height="170" fill="{INK}"/>
<rect x="60" y="442" width="480" height="14" rx="5" fill="#8A5A44"/>
<rect x="130" y="224" width="150" height="14" rx="5" fill="#FFFFFF"/>
<rect x="130" y="206" width="150" height="14" rx="5" fill="#FFFFFF"/>
<rect x="130" y="188" width="150" height="14" rx="5" fill="#FFFFFF"/>
<rect x="330" y="206" width="130" height="32" rx="16" fill="#0E6B66"/>
<path d="M150 442 v-70 q0-30 45-30 q45 0 45 30 v70z" fill="#FFFFFF"/>
<path d="M290 442 v-60 q0-26 40-26 q40 0 40 26 v60z" fill="#F2C94C"/>""")

    jars = ""
    for x, h, fill in [(70, 230, "#F5EAC8"), (225, 290, "#E07A5F"), (380, 190, "#0E6B66")]:
        top = 470 - h
        jars += (
            f'<rect x="{x}" y="{top}" width="150" height="{h}" rx="20" fill="#FFFFFF" fill-opacity=".75" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x + 8}" y="{top + h // 3}" width="134" height="{h - h // 3 - 8}" rx="14" fill="{fill}"/>'
            f'<rect x="{x + 10}" y="{top - 30}" width="130" height="30" rx="8" fill="{INK}"/>'
        )
    imgs["jar-set.svg"] = svg(p["jar-set.svg"], jars)

    slots = ""
    for k in range(6):
        slots += f'<rect x="{80 + k * 72}" y="260" width="58" height="150" rx="8" fill="#F1ECF8"/>'
    imgs["cutlery-tray.svg"] = svg(p["cutlery-tray.svg"], f"""
<rect x="55" y="235" width="490" height="200" rx="18" fill="#6B5B95"/>{slots}
<rect x="100" y="180" width="12" height="150" rx="6" fill="{INK}"/>
<ellipse cx="106" cy="176" rx="16" ry="22" fill="{INK}"/>
<rect x="244" y="190" width="12" height="140" rx="6" fill="#0E6B66"/>
<ellipse cx="250" cy="186" rx="16" ry="22" fill="#0E6B66"/>
<rect x="388" y="170" width="12" height="160" rx="6" fill="#E07A5F"/>
<ellipse cx="394" cy="166" rx="16" ry="22" fill="#E07A5F"/>""")

    mugs = f'<rect x="70" y="140" width="460" height="30" rx="8" fill="{INK}"/>'
    for k, col in enumerate(["#FFFFFF", "#0E6B66", "#F2C94C", "#E07A5F"]):
        x = 105 + k * 105
        mugs += (
            f'<rect x="{x + 28}" y="170" width="6" height="60" fill="{INK}"/>'
            f'<rect x="{x}" y="228" width="62" height="84" rx="10" fill="{col}"/>'
            f'<path d="M{x + 62} 244 q34 0 34 28 q0 28 -34 28" fill="none" stroke="{col}" stroke-width="10"/>'
        )
    imgs["mug-rack.svg"] = svg(p["mug-rack.svg"], mugs)

    for name, content in imgs.items():
        write(f"images/{name}", content)


# ------------------------------------------------------------------ layout
def head(title, desc, path, extra=""):
    gtm = CFG.get("gtm_id", "").strip()
    gtm_head = ""
    gtm_body = ""
    if gtm:
        gtm_head = (
            "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),"
            "event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';"
            "j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);"
            f"}})(window,document,'script','dataLayer','{gtm}');</script>"
        )
        gtm_body = (
            f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gtm}" height="0" width="0" '
            'style="display:none;visibility:hidden"></iframe></noscript>'
        )
    store_js = json.dumps(
        {"name": NAME, "currency": CUR, "code": CFG["currency_code"], "whatsapp": CFG["whatsapp"]}
    )
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{URL}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{URL}{path}">
<meta property="og:site_name" content="{NAME}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=Instrument+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/css/style.css">
<script>window.STORE={store_js};window.dataLayer=window.dataLayer||[];</script>
{gtm_head}
{extra}
</head>
<body>
{gtm_body}
"""
    return page


def header():
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="/">{NAME}</a>
    <nav class="nav" aria-label="Main">
      <a class="hide-sm" href="/#products">Shop</a>
      <a class="hide-sm" href="/about.html">About</a>
      <a class="hide-sm" href="/shipping-returns.html">Shipping</a>
      <button class="cart-btn" data-cart-open aria-label="Open cart">Cart<span class="cart-count" data-cart-count>0</span></button>
    </nav>
  </div>
</header>
"""


def footer():
    return f"""
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <strong>{NAME}</strong><br>{escape(CFG['tagline'])}.<br>
      <small>Practice store for learning digital marketing. Not a real shop.</small>
    </div>
    <nav aria-label="Footer">
      <a href="/about.html">About</a>
      <a href="/shipping-returns.html">Shipping and returns</a>
      <a href="/checkout.html">Checkout</a>
    </nav>
  </div>
</footer>

<div class="overlay" id="overlay"></div>
<aside class="drawer" id="drawer" aria-hidden="true" aria-label="Shopping cart">
  <div class="drawer-head">
    <h2>Your cart</h2>
    <button class="icon-btn" data-cart-close aria-label="Close cart">&times;</button>
  </div>
  <div class="drawer-items" id="drawer-items"></div>
  <div class="drawer-foot" id="drawer-foot" hidden>
    <div class="line"><span>Subtotal</span><span id="drawer-total"></span></div>
    <a class="btn block" href="/checkout.html">Go to checkout</a>
  </div>
</aside>
<script src="/js/store.js"></script>
</body>
</html>
"""


def page(title, desc, path, body, extra=""):
    return head(title, desc, path, extra) + header() + f'<main id="main">\n{body}\n</main>' + footer()


def add_button(p, label="Add to cart", cls="btn"):
    return (
        f'<button class="{cls}" data-add data-id="{p["slug"]}" data-name="{escape(p["name"])}" '
        f'data-price="{p["price"]}" data-img="/images/{p["image"]}">{label}</button>'
    )


def price_html(p):
    old = f'<span class="old">{money(p["old_price"])}</span>' if p["old_price"] else ""
    return f'<div class="price-row"><span class="price">{money(p["price"])}</span>{old}</div>'


def card(p):
    return f"""<article class="card" data-cat="{p['category']}">
  <a class="thumb" href="/products/{p['slug']}.html"><img src="/images/{p['image']}" alt="{escape(p['name'])}" width="600" height="600" loading="lazy"></a>
  <div class="card-body">
    <h3><a href="/products/{p['slug']}.html">{escape(p['name'])}</a></h3>
    <p class="short">{escape(p['short'])}</p>
    {price_html(p)}
    {add_button(p)}
  </div>
</article>"""


# ------------------------------------------------------------------ pages
def build_home():
    hero_imgs = "".join(
        f'<img src="/images/{p["image"]}" alt="{escape(p["name"])}" width="600" height="600">' for p in PRODUCTS[:4]
    )
    filters = '<button data-filter="all" aria-pressed="true">All</button>' + "".join(
        f'<button data-filter="{c}" aria-pressed="false">{c}</button>' for c in CFG["categories"]
    )
    cards = "\n".join(card(p) for p in PRODUCTS)
    faqs = [
        ("How long does delivery take?", "Orders reach most major cities in 3 to 5 working days and other areas in 5 to 8 working days."),
        ("Can I pay on delivery?", "Yes. Cash on delivery is available across Pakistan. You pay the rider when the parcel arrives."),
        ("What if an organizer does not fit my drawer or cabinet?", "Measure your space against the size listed on the product page. If it still does not fit, message us within 7 days of delivery and we will arrange a return or exchange."),
        ("How do I place an order?", "Add items to your cart, fill in your delivery details at checkout, and send the order to us on WhatsApp. We confirm it by message."),
    ]
    faq_html = "\n".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    org = {
        "@context": "https://schema.org",
        "@type": "Store",
        "name": NAME,
        "url": URL + "/",
        "description": CFG["tagline"],
    }
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
        ],
    }
    extra = (
        f'<script type="application/ld+json">{json.dumps(org)}</script>\n'
        f'<script type="application/ld+json">{json.dumps(faq_ld)}</script>'
    )
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>Everything in its place.</h1>
      <p class="lead">Drawer trays, shelf risers and pantry jars sized for small Pakistani kitchens. Cash on delivery, order in two minutes on WhatsApp.</p>
      <div class="hero-actions">
        <a class="btn" href="#products">Shop organizers</a>
        <a class="btn ghost" href="/shipping-returns.html">Delivery and returns</a>
      </div>
    </div>
    <div class="hero-board" aria-hidden="true">{hero_imgs}</div>
  </div>
</section>

<section id="products">
  <div class="wrap">
    <div class="section-head">
      <h2>Kitchen organizers</h2>
      <div class="filters" role="group" aria-label="Filter products">{filters}</div>
    </div>
    <div class="grid">
{cards}
    </div>
  </div>
</section>

<section>
  <div class="wrap facts">
    <div><h3>Sized for real kitchens</h3><p>Every product lists exact measurements, so you know it fits before you order.</p></div>
    <div><h3>Pay when it arrives</h3><p>Cash on delivery across Pakistan. No card needed.</p></div>
    <div><h3>Seven-day returns</h3><p>If it does not fit or arrives damaged, message us and we will fix it.</p></div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Questions</h2>
    {faq_html}
  </div>
</section>"""
    write(
        "index.html",
        page(
            f"{NAME} | Kitchen organizers for small kitchens in Pakistan",
            "Drawer organizers, spice racks, shelf risers and airtight jars for small kitchens. Cash on delivery across Pakistan.",
            "/",
            body,
            extra,
        ),
    )


def build_products():
    for p in PRODUCTS:
        feats = "".join(f"<li>{escape(f)}</li>" for f in p["features"])
        badge = ""
        if p["old_price"]:
            off = round((1 - p["price"] / p["old_price"]) * 100)
            badge = f'<span class="badge">{off}% off</span>'
        ld = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": p["name"],
            "description": p["description"],
            "image": f"{URL}/images/{p['image']}",
            "category": p["category"],
            "brand": {"@type": "Brand", "name": NAME},
            "offers": {
                "@type": "Offer",
                "url": f"{URL}/products/{p['slug']}.html",
                "priceCurrency": CFG["currency_code"],
                "price": str(p["price"]),
                "availability": "https://schema.org/InStock",
            },
        }
        extra = f'<script type="application/ld+json">{json.dumps(ld)}</script>'
        related = "\n".join([card(r) for r in PRODUCTS if r["slug"] != p["slug"]][:3])
        body = f"""
<div class="wrap">
  <p class="crumbs"><a href="/">Home</a> / <a href="/#products">Shop</a> / {escape(p['name'])}</p>
  <div class="product" data-product="{p['slug']}" data-name="{escape(p['name'])}" data-price="{p['price']}">
    <img src="/images/{p['image']}" alt="{escape(p['name'])}" width="600" height="600">
    <div>
      {badge}
      <h1 style="font-size:clamp(2rem,4vw,2.8rem)">{escape(p['name'])}</h1>
      {price_html(p)}
      <p style="margin-top:1rem">{escape(p['description'])}</p>
      <ul>{feats}</ul>
      {add_button(p, "Add to cart")}
      <p class="buy-note">Cash on delivery. Delivery in 3 to 8 working days. 7-day returns.</p>
    </div>
  </div>
  <section style="padding-top:1rem">
    <h2>You may also like</h2>
    <div class="grid">{related}</div>
  </section>
</div>"""
        write(
            f"products/{p['slug']}.html",
            page(
                f"{p['name']} | {NAME}",
                f"{p['short']} {money(p['price'])}. Cash on delivery across Pakistan.",
                f"/products/{p['slug']}.html",
                body,
                extra,
            ),
        )


def build_checkout():
    body = """
<div class="wrap">
  <h1 style="font-size:clamp(2rem,4vw,2.8rem);padding-top:2rem">Checkout</h1>
  <div class="checkout">
    <div>
      <form id="order-form">
        <div class="field"><label for="name">Full name</label><input id="name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="phone">Phone number</label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="03XX XXXXXXX" required></div>
        <div class="field"><label for="city">City</label><input id="city" name="city" autocomplete="address-level2" required></div>
        <div class="field"><label for="address">Delivery address</label><textarea id="address" name="address" rows="3" autocomplete="street-address" required></textarea></div>
        <div class="field"><label for="note">Note for us (optional)</label><input id="note" name="note"></div>
        <button class="btn" type="submit">Send order on WhatsApp</button>
        <p class="buy-note">You pay cash when the parcel arrives. We confirm your order on WhatsApp.</p>
      </form>
      <div class="done" id="done" hidden>
        <h2>Order ready to send</h2>
        <p>WhatsApp should open with your order. If it did not, use the button below, then press send.</p>
        <a class="btn" id="wa-link" href="#" target="_blank" rel="noopener">Open WhatsApp</a>
      </div>
    </div>
    <aside class="summary">
      <h2 style="font-size:1.4rem">Your order</h2>
      <div id="summary-items"></div>
      <div class="line total"><span>Total</span><span id="summary-total"></span></div>
    </aside>
  </div>
</div>"""
    write(
        "checkout.html",
        page(f"Checkout | {NAME}", "Send your order on WhatsApp. Cash on delivery.", "/checkout.html", body,
             '<meta name="robots" content="noindex">'),
    )


def build_info():
    about = f"""
<div class="wrap prose">
  <h1>About {NAME}</h1>
  <p>{NAME} sells kitchen organizers that fit small kitchens. We started with one question: why is it so hard to find a drawer tray or shelf riser that fits a normal Pakistani kitchen?</p>
  <p>Every product page lists exact measurements, so you can check your drawer or cabinet before you order.</p>
  <h2>This is a practice store</h2>
  <p>This site was built as a learning project for digital marketing: SEO, analytics, Meta Ads and Google Ads. The products and prices are examples, and no real orders are fulfilled.</p>
  <p><a class="btn" href="/#products">See the products</a></p>
</div>"""
    write("about.html", page(f"About | {NAME}", f"About {NAME}, a kitchen organizer store for small kitchens.", "/about.html", about))

    ship = """
<div class="wrap prose">
  <h1>Shipping and returns</h1>
  <h2>Delivery</h2>
  <p>Major cities: 3 to 5 working days. Other areas: 5 to 8 working days. You will get a message on WhatsApp when your parcel is dispatched.</p>
  <h2>Payment</h2>
  <p>Cash on delivery. You pay the rider when the parcel arrives.</p>
  <h2>Returns and exchanges</h2>
  <p>If an item arrives damaged or does not fit, message us on WhatsApp within 7 days of delivery. Keep the item unused and in its packaging, and we will arrange a return or exchange.</p>
  <h2>Contact</h2>
  <p>WhatsApp or email us at the details on the checkout page and footer. We reply within one working day.</p>
</div>"""
    write("shipping-returns.html", page(f"Shipping and returns | {NAME}", "Delivery times, cash on delivery and 7-day returns.", "/shipping-returns.html", ship))

    nf = """
<div class="wrap prose">
  <h1>Page not found</h1>
  <p>This page does not exist or has moved. Go back to the shop and pick up where you left off.</p>
  <p><a class="btn" href="/">Back to the shop</a></p>
</div>"""
    write("404.html", page(f"Page not found | {NAME}", "Page not found.", "/404.html", nf, '<meta name="robots" content="noindex">'))


def build_seo_files():
    urls = ["/", "/about.html", "/shipping-returns.html"] + [f"/products/{p['slug']}.html" for p in PRODUCTS]
    items = "\n".join(f"  <url><loc>{URL}{u}</loc></url>" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /checkout.html\nSitemap: {URL}/sitemap.xml\n")


if __name__ == "__main__":
    make_images()
    build_home()
    build_products()
    build_checkout()
    build_info()
    build_seo_files()
    print(f"Built {len(PRODUCTS)} products. Site URL set to {URL}")
