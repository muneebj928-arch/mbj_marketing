(function () {
  var S = window.STORE || {};
  var KEY = "nook_cart_v1";

  function $(s, r) { return (r || document).querySelector(s); }
  function $all(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function money(n) { return S.currency + " " + Number(n).toLocaleString("en-PK"); }

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; }
  }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {}
  }
  var cart = load();

  // Events for Google Tag Manager (GA4 and Meta Pixel can read these later)
  function track(event, items, value) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: event,
      ecommerce: { currency: S.code, value: value || 0, items: items }
    });
  }
  function gaItem(i) {
    return { item_id: i.id, item_name: i.name, price: i.price, quantity: i.qty || 1 };
  }

  function total() {
    return cart.reduce(function (a, i) { return a + i.price * i.qty; }, 0);
  }
  function count() {
    return cart.reduce(function (a, i) { return a + i.qty; }, 0);
  }

  // ---- cart drawer ----
  var drawer = $("#drawer"), overlay = $("#overlay");

  function openCart() {
    if (!drawer) return;
    drawer.classList.add("open");
    overlay.classList.add("open");
    drawer.setAttribute("aria-hidden", "false");
    var c = $("[data-cart-close]", drawer);
    if (c) c.focus();
  }
  function closeCart() {
    if (!drawer) return;
    drawer.classList.remove("open");
    overlay.classList.remove("open");
    drawer.setAttribute("aria-hidden", "true");
  }

  function render() {
    $all("[data-cart-count]").forEach(function (el) { el.textContent = count(); });
    var box = $("#drawer-items");
    var foot = $("#drawer-foot");
    if (!box) return;
    if (!cart.length) {
      box.innerHTML = '<p class="empty">Your cart is empty. Add an organizer to get started.</p>';
      if (foot) foot.hidden = true;
      return;
    }
    if (foot) foot.hidden = false;
    box.innerHTML = cart.map(function (i) {
      return '<div class="cart-item">' +
        '<img src="' + i.img + '" alt="" width="64" height="64">' +
        '<div><div class="nm">' + i.name + '</div>' +
        '<div class="qty"><button data-dec="' + i.id + '" aria-label="Remove one">&minus;</button>' +
        '<span>' + i.qty + '</span>' +
        '<button data-inc="' + i.id + '" aria-label="Add one">+</button></div>' +
        '<button class="rm" data-rm="' + i.id + '">Remove</button></div>' +
        '<div>' + money(i.price * i.qty) + '</div></div>';
    }).join("");
    var t = $("#drawer-total");
    if (t) t.textContent = money(total());
  }

  function find(id) {
    for (var k = 0; k < cart.length; k++) if (cart[k].id === id) return cart[k];
    return null;
  }

  function add(btn) {
    var id = btn.getAttribute("data-id");
    var item = find(id);
    if (item) { item.qty += 1; }
    else {
      item = {
        id: id,
        name: btn.getAttribute("data-name"),
        price: Number(btn.getAttribute("data-price")),
        img: btn.getAttribute("data-img"),
        qty: 1
      };
      cart.push(item);
    }
    save(); render(); openCart();
    track("add_to_cart", [gaItem({ id: item.id, name: item.name, price: item.price, qty: 1 })], item.price);
  }

  document.addEventListener("click", function (e) {
    var t = e.target;
    var addBtn = t.closest && t.closest("[data-add]");
    if (addBtn) { add(addBtn); return; }
    if (t.closest && t.closest("[data-cart-open]")) { openCart(); return; }
    if (t.closest && (t.closest("[data-cart-close]") || t === overlay)) { closeCart(); return; }
    var inc = t.getAttribute && t.getAttribute("data-inc");
    var dec = t.getAttribute && t.getAttribute("data-dec");
    var rm = t.getAttribute && t.getAttribute("data-rm");
    if (inc) { find(inc).qty += 1; save(); render(); renderCheckout(); }
    if (dec) {
      var it = find(dec);
      it.qty -= 1;
      if (it.qty <= 0) cart = cart.filter(function (x) { return x.id !== dec; });
      save(); render(); renderCheckout();
    }
    if (rm) { cart = cart.filter(function (x) { return x.id !== rm; }); save(); render(); renderCheckout(); }
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeCart(); });

  // ---- category filter on home page ----
  $all("[data-filter]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var f = btn.getAttribute("data-filter");
      $all("[data-filter]").forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
      $all(".card[data-cat]").forEach(function (c) {
        c.hidden = !(f === "all" || c.getAttribute("data-cat") === f);
      });
    });
  });

  // ---- product page view event ----
  var pv = $("[data-product]");
  if (pv) {
    track("view_item", [{
      item_id: pv.getAttribute("data-product"),
      item_name: pv.getAttribute("data-name"),
      price: Number(pv.getAttribute("data-price")),
      quantity: 1
    }], Number(pv.getAttribute("data-price")));
  }

  // ---- checkout page ----
  var form = $("#order-form");
  function renderCheckout() {
    var list = $("#summary-items");
    if (!list) return;
    if (!cart.length) {
      list.innerHTML = '<p class="empty">Your cart is empty. <a href="/#products">Browse products</a></p>';
      $("#summary-total").textContent = money(0);
      if (form) form.querySelector("button[type=submit]").disabled = true;
      return;
    }
    if (form) form.querySelector("button[type=submit]").disabled = false;
    list.innerHTML = cart.map(function (i) {
      return '<div class="line"><span>' + i.name + ' &times; ' + i.qty + '</span><span>' + money(i.price * i.qty) + '</span></div>';
    }).join("");
    $("#summary-total").textContent = money(total());
  }

  if (form) {
    renderCheckout();
    track("begin_checkout", cart.map(gaItem), total());

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!cart.length) return;
      var d = new FormData(form);
      var lines = cart.map(function (i) { return "- " + i.name + " x " + i.qty + " = " + money(i.price * i.qty); });
      var msg =
        "New order from " + S.name + " website\n\n" +
        lines.join("\n") + "\n\nTotal: " + money(total()) + " (Cash on delivery)\n\n" +
        "Name: " + d.get("name") + "\n" +
        "Phone: " + d.get("phone") + "\n" +
        "City: " + d.get("city") + "\n" +
        "Address: " + d.get("address") + "\n" +
        (d.get("note") ? "Note: " + d.get("note") + "\n" : "");
      var url = "https://wa.me/" + S.whatsapp + "?text=" + encodeURIComponent(msg);

      track("purchase", cart.map(gaItem), total());
      $("#wa-link").setAttribute("href", url);
      form.hidden = true;
      $("#done").hidden = false;
      var s = $(".summary"); if (s) s.hidden = true;
      cart = []; save(); render();
      window.open(url, "_blank", "noopener");
    });
  }

  render();
})();
