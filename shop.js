const SHOP_STORAGE_KEY = "scf_demo_cart";
const PAYMENT_METHOD_KEY = "scf_demo_payment_method";

const SHOP_PRODUCTS = [
  {
    id: "home-jersey-26",
    title: "Home Jersey 26",
    price: 89,
    compareAt: 99,
    tag: "Matchday",
    category: "jersey",
    featured: true,
    image: "../assets/product-jersey.jpg",
    alt: "Rotes Jersey als Produktfoto",
    rating: "4.9 / 5",
    colors: ["Rot", "Schwarz"],
    sizes: ["S", "M", "L", "XL"],
    description:
      "Hero-Produkt für eine Fanshop-Startseite mit starker Bildwirkung, klarer Größenauswahl und hoher Kaufintention.",
    bullets: [
      "Kategorie: Trikot",
      "Größenlogik für den Produktflow",
      "Bundle-fähig für Spieltage"
    ]
  },
  {
    id: "away-jersey-night",
    title: "Away Jersey Night",
    price: 84,
    compareAt: 94,
    tag: "Drop",
    category: "jersey",
    featured: true,
    image: "../assets/product-jersey.jpg",
    alt: "Trikot als Demo für Away Jersey",
    rating: "4.8 / 5",
    colors: ["Weiß", "Schwarz"],
    sizes: ["S", "M", "L", "XL"],
    description:
      "Zweites Trikot als Beispiel für eine saisonale Produktlinie mit klarer Hero-Platzierung und Preislogik.",
    bullets: [
      "Kategorie: Trikot",
      "Für Launches und Saisondrops",
      "Klar auf Landingpages einsetzbar"
    ]
  },
  {
    id: "matchday-scarf",
    title: "Matchday Scarf",
    price: 29,
    compareAt: 34,
    tag: "Fanwear",
    category: "accessories",
    featured: true,
    image: "../assets/product-scarf.jpg",
    alt: "Schal als Beispielprodukt",
    rating: "4.8 / 5",
    colors: ["Rot", "Weiß"],
    sizes: ["One Size"],
    description:
      "Emotionales Zusatzprodukt für Matchday-Aktionen, Bundles und schnelle Impulskäufe im Fanshop.",
    bullets: [
      "Kategorie: Accessoire",
      "Gut für Cross-Selling",
      "Sichtbar auf Aktionsflächen"
    ]
  },
  {
    id: "blackout-hoodie",
    title: "Blackout Hoodie",
    price: 69,
    compareAt: 79,
    tag: "Core",
    category: "lifestyle",
    featured: true,
    image: "../assets/product-rack.jpg",
    alt: "Kleidung auf Kleiderständer als Hoodie-Demo",
    rating: "4.8 / 5",
    colors: ["Schwarz", "Grau"],
    sizes: ["S", "M", "L", "XL"],
    description:
      "Lifestyle-Piece für Fans, die ein reduziertes, modernes Vereinsprodukt mit Alltagsbezug suchen.",
    bullets: [
      "Kategorie: Hoodie",
      "Ideal für Daily Wear",
      "Stark für Editorial Sections"
    ]
  },
  {
    id: "stadium-runner",
    title: "Stadium Runner",
    price: 74,
    compareAt: 89,
    tag: "Lifestyle",
    category: "lifestyle",
    featured: false,
    image: "../assets/product-sneaker.jpg",
    alt: "Sneaker als Lifestyle-Produkt",
    rating: "4.7 / 5",
    colors: ["Schwarz", "Grau"],
    sizes: ["40", "41", "42", "43", "44"],
    description:
      "Lifestyle-Produkt für Sortimentsbreite, Social Assets und Zielgruppen außerhalb des klassischen Spieltags.",
    bullets: [
      "Kategorie: Lifestyle",
      "Visuell stark für Social Content",
      "Geeignet für Landingpage-Features"
    ]
  },
  {
    id: "city-supporter-bag",
    title: "City Supporter Bag",
    price: 34,
    compareAt: 39,
    tag: "Daily",
    category: "accessories",
    featured: false,
    image: "../assets/product-rack.jpg",
    alt: "Produktfoto von Kleidung und Stofftaschen",
    rating: "4.8 / 5",
    colors: ["Natur", "Schwarz"],
    sizes: ["One Size"],
    description:
      "Alltagsnahes Merch-Produkt für Fans, die Verein, Stil und Nutzwert in einem modernen Sortiment verbinden wollen.",
    bullets: [
      "Kategorie: Tasche",
      "Gute Geschenkoption",
      "Alltagsprodukt mit Fanbezug"
    ]
  },
  {
    id: "stadium-cap",
    title: "Stadium Cap",
    price: 24,
    compareAt: 29,
    tag: "Accessory",
    category: "accessories",
    featured: false,
    image: "../assets/product-scarf.jpg",
    alt: "Accessoire als Demo für eine Cap",
    rating: "4.6 / 5",
    colors: ["Schwarz", "Rot"],
    sizes: ["One Size"],
    description:
      "Leichtes Zusatzprodukt für Bundles, Spieltagssortimente und Shop-Aktionen mit niedriger Kaufbarriere.",
    bullets: [
      "Kategorie: Cap",
      "Impulsstarkes Add-on",
      "Gut für Aktionsbanner"
    ]
  },
  {
    id: "travel-tumbler",
    title: "Travel Tumbler",
    price: 19,
    compareAt: 24,
    tag: "Gift",
    category: "accessories",
    featured: false,
    image: "../assets/mock-fanshop.jpg",
    alt: "Shop-Visual als Demo für ein Geschenkprodukt",
    rating: "4.7 / 5",
    colors: ["Schwarz", "Silber"],
    sizes: ["450 ml"],
    description:
      "Kleiner Geschenkartikel für Aktionsseiten, Geschenk-Guides und Merch-Kombinationen mit höherem Warenkorbwert.",
    bullets: [
      "Kategorie: Geschenkartikel",
      "Niedrige Einstiegshürde",
      "Gut für Geschenk-Guides"
    ]
  }
];

function defaultVariant(product) {
  return {
    size: product.sizes?.[0] || "",
    color: product.colors?.[0] || ""
  };
}

function normalizeCartItem(item) {
  return {
    id: item.id,
    quantity: Number(item.quantity) > 0 ? Number(item.quantity) : 1,
    size: item.size || "",
    color: item.color || ""
  };
}

function readCart() {
  try {
    const raw = JSON.parse(localStorage.getItem(SHOP_STORAGE_KEY) || "[]");
    return Array.isArray(raw) ? raw.map(normalizeCartItem).filter((item) => item.id) : [];
  } catch {
    return [];
  }
}

function writeCart(cart) {
  localStorage.setItem(SHOP_STORAGE_KEY, JSON.stringify(cart));
}

function getProduct(productId) {
  return SHOP_PRODUCTS.find((product) => product.id === productId);
}

function getVariantLabel(item) {
  const parts = [item.size, item.color].filter(Boolean);
  return parts.length ? parts.join(" / ") : "Standard";
}

function getActivePaymentMethod() {
  return sessionStorage.getItem(PAYMENT_METHOD_KEY) || "stripe";
}

function setActivePaymentMethod(method) {
  sessionStorage.setItem(PAYMENT_METHOD_KEY, method);
}

function cartSubtotal(cart) {
  return cart.reduce((total, item) => {
    const product = getProduct(item.id);
    return product ? total + product.price * item.quantity : total;
  }, 0);
}

function formatCurrency(value) {
  return `${value.toFixed(2).replace(".", ",")} EUR`;
}

function normalize(text) {
  return (text || "")
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function showToast(message) {
  const toast = document.getElementById("shopToast");
  if (!toast) {
    return;
  }

  toast.textContent = message;
  toast.hidden = false;
  window.clearTimeout(showToast.timeoutId);
  showToast.timeoutId = window.setTimeout(() => {
    toast.hidden = true;
  }, 2200);
}

function addToCart(productId, options = {}) {
  const product = getProduct(productId);
  if (!product) {
    return;
  }

  const variant = defaultVariant(product);
  const size = options.size || variant.size;
  const color = options.color || variant.color;
  const quantity = Math.max(1, Number(options.quantity) || 1);
  const cart = readCart();
  const existing = cart.find(
    (item) => item.id === productId && item.size === size && item.color === color
  );

  if (existing) {
    existing.quantity += quantity;
  } else {
    cart.push({ id: productId, quantity, size, color });
  }

  writeCart(cart);
  renderCart();
  renderCheckout();
  showToast(`${product.title} wurde in den Warenkorb gelegt.`);
}

function changeQuantity(productId, size, color, delta) {
  const cart = readCart()
    .map((item) => {
      if (item.id === productId && item.size === size && item.color === color) {
        return { ...item, quantity: item.quantity + delta };
      }
      return item;
    })
    .filter((item) => item.quantity > 0);

  writeCart(cart);
  renderCart();
  renderCheckout();
}

function openElement(element) {
  if (element) {
    element.hidden = false;
  }
}

function closeElement(element) {
  if (element) {
    element.hidden = true;
  }
}

function productCardMarkup(product) {
  const compareMarkup = product.compareAt
    ? `<span class="shop-card__compare">${formatCurrency(product.compareAt)}</span>`
    : "";

  return `
    <img src="${product.image}" alt="${product.alt}" loading="lazy" />
    <div class="shop-card__topline">
      <span class="shop-card__tag">${product.tag}</span>
      <span class="shop-card__rating">${product.rating}</span>
    </div>
    <h3>${product.title}</h3>
    <p>${product.description}</p>
    <div class="product-meta">
      ${product.bullets.slice(0, 2).map((item) => `<span class="product-chip">${item}</span>`).join("")}
    </div>
    <div class="shop-card__meta">
      <div class="shop-card__price-group">
        <span class="shop-card__price">${formatCurrency(product.price)}</span>
        ${compareMarkup}
      </div>
      <span class="shop-toolbar__hint">${product.category}</span>
    </div>
    <div class="shop-card__actions">
      <button class="button button--card" type="button" data-details="${product.id}">Details</button>
      <button class="button button--primary" type="button" data-add="${product.id}">In den Warenkorb</button>
    </div>
  `;
}

function renderShopProducts() {
  const grid = document.getElementById("shopGrid");
  if (!grid) {
    return;
  }

  const search = document.getElementById("shopSearch");
  const chipButtons = [...document.querySelectorAll("[data-shop-filter]")];
  const emptyState = document.getElementById("shopEmptyState");
  let activeFilter = "all";

  function applyFilters() {
    const term = normalize(search?.value || "");
    let visible = 0;

    [...grid.children].forEach((card) => {
      const matchesFilter =
        activeFilter === "all" || card.dataset.category === activeFilter;
      const matchesSearch = term === "" || normalize(card.dataset.search).includes(term);
      const show = matchesFilter && matchesSearch;
      card.hidden = !show;
      if (show) {
        visible += 1;
      }
    });

    if (emptyState) {
      emptyState.hidden = visible !== 0;
    }
  }

  grid.innerHTML = "";

  SHOP_PRODUCTS.forEach((product) => {
    const card = document.createElement("article");
    card.className = "shop-card";
    card.dataset.category = product.category;
    card.dataset.search = [
      product.title,
      product.tag,
      product.description,
      product.category,
      product.colors.join(" "),
      product.sizes.join(" ")
    ].join(" ");
    card.innerHTML = productCardMarkup(product);
    grid.appendChild(card);
  });

  grid.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
      return;
    }

    const detailId = target.dataset.details;
    if (detailId) {
      renderProductModal(detailId);
    }

    const addId = target.dataset.add;
    if (addId) {
      addToCart(addId);
      openElement(document.getElementById("cartDrawerShell"));
    }
  });

  chipButtons.forEach((button) => {
    button.addEventListener("click", () => {
      activeFilter = button.dataset.shopFilter || "all";
      chipButtons.forEach((chip) => chip.classList.toggle("is-active", chip === button));
      applyFilters();
    });
  });

  if (search) {
    search.addEventListener("input", applyFilters);
  }

  applyFilters();
}

function renderRecommendedProducts() {
  const grid = document.getElementById("recommendedGrid");
  if (!grid) {
    return;
  }

  grid.innerHTML = SHOP_PRODUCTS.filter((product) => product.featured)
    .slice(0, 3)
    .map(
      (product) => `
        <article class="recommendation-card">
          <img src="${product.image}" alt="${product.alt}" loading="lazy" />
          <div class="recommendation-card__copy">
            <span class="shop-card__tag">${product.tag}</span>
            <h3>${product.title}</h3>
            <p>${product.description}</p>
            <div class="summary-line">
              <span>${formatCurrency(product.price)}</span>
              <button class="button button--card" type="button" data-add="${product.id}">Quick Add</button>
            </div>
          </div>
        </article>
      `
    )
    .join("");

  grid.querySelectorAll("[data-add]").forEach((button) => {
    button.addEventListener("click", () => {
      addToCart(button.dataset.add);
      openElement(document.getElementById("cartDrawerShell"));
    });
  });
}

function renderProductModal(productId) {
  const product = getProduct(productId);
  const shell = document.getElementById("productModalShell");
  const container = document.getElementById("productModal");

  if (!product || !shell || !container) {
    return;
  }

  const initialVariant = defaultVariant(product);
  let selectedSize = initialVariant.size;
  let selectedColor = initialVariant.color;
  let quantity = 1;

  container.innerHTML = `
    <div class="product-modal__card">
      <img src="${product.image}" alt="${product.alt}" />
      <div class="product-modal__copy">
        <div class="shop-card__topline">
          <span class="shop-card__tag">${product.tag}</span>
          <span class="shop-card__rating">${product.rating}</span>
        </div>
        <div>
          <h2>${product.title}</h2>
          <p class="project-copy">${product.description}</p>
        </div>
        <div class="product-meta">
          ${product.bullets.map((item) => `<span class="product-chip">${item}</span>`).join("")}
        </div>
        <div class="shop-card__price-group">
          <strong class="shop-card__price">${formatCurrency(product.price)}</strong>
          ${product.compareAt ? `<span class="shop-card__compare">${formatCurrency(product.compareAt)}</span>` : ""}
        </div>
        <div class="variant-block">
          <p class="eyebrow">Größe</p>
          <div class="variant-row">
            ${product.sizes
              .map(
                (size) =>
                  `<button class="size-chip${size === selectedSize ? " is-active" : ""}" type="button" data-size="${size}">${size}</button>`
              )
              .join("")}
          </div>
        </div>
        <div class="variant-block">
          <p class="eyebrow">Farbe</p>
          <div class="variant-row">
            ${product.colors
              .map(
                (color) =>
                  `<button class="color-chip${color === selectedColor ? " is-active" : ""}" type="button" data-color="${color}">${color}</button>`
              )
              .join("")}
          </div>
        </div>
        <div class="qty-row">
          <button class="qty-button" type="button" id="qtyMinus">-</button>
          <strong id="qtyValue">1</strong>
          <button class="qty-button" type="button" id="qtyPlus">+</button>
        </div>
        <div class="button-row">
          <button class="button button--primary" type="button" id="modalAddToCart">In den Warenkorb</button>
          <button class="button button--ghost" type="button" id="closeProductModal">Schließen</button>
        </div>
      </div>
    </div>
  `;

  openElement(shell);

  const qtyValue = document.getElementById("qtyValue");
  const setActive = (selector, value, dataKey) => {
    container.querySelectorAll(selector).forEach((button) => {
      button.classList.toggle("is-active", button.dataset[dataKey] === value);
    });
  };

  container.querySelectorAll("[data-size]").forEach((button) => {
    button.addEventListener("click", () => {
      selectedSize = button.dataset.size || "";
      setActive(".size-chip", selectedSize, "size");
    });
  });

  container.querySelectorAll("[data-color]").forEach((button) => {
    button.addEventListener("click", () => {
      selectedColor = button.dataset.color || "";
      setActive(".color-chip", selectedColor, "color");
    });
  });

  document.getElementById("qtyMinus").addEventListener("click", () => {
    quantity = Math.max(1, quantity - 1);
    qtyValue.textContent = String(quantity);
  });

  document.getElementById("qtyPlus").addEventListener("click", () => {
    quantity += 1;
    qtyValue.textContent = String(quantity);
  });

  document.getElementById("modalAddToCart").addEventListener("click", () => {
    addToCart(product.id, { quantity, size: selectedSize, color: selectedColor });
    closeElement(shell);
    openElement(document.getElementById("cartDrawerShell"));
  });

  document.getElementById("closeProductModal").addEventListener("click", () => {
    closeElement(shell);
  });
}

function renderCart() {
  const badge = document.getElementById("cartBadge");
  const list = document.getElementById("cartList");
  const subtotal = document.getElementById("cartSubtotal");

  if (!badge || !list || !subtotal) {
    return;
  }

  const cart = readCart();
  const totalQuantity = cart.reduce((sum, item) => sum + item.quantity, 0);
  badge.textContent = String(totalQuantity);

  if (cart.length === 0) {
    list.innerHTML = `<p class="cart-empty">Der Warenkorb ist aktuell leer.</p>`;
    subtotal.textContent = formatCurrency(0);
    return;
  }

  list.innerHTML = cart
    .map((item) => {
      const product = getProduct(item.id);
      if (!product) {
        return "";
      }

      return `
        <article class="cart-item">
          <img src="${product.image}" alt="${product.alt}" />
          <div class="cart-item__copy">
            <strong>${product.title}</strong>
            <span>${getVariantLabel(item)}</span>
            <span>${formatCurrency(product.price)} x ${item.quantity}</span>
            <div class="button-row">
              <button class="button button--secondary" type="button" data-cart-id="${product.id}" data-cart-size="${item.size}" data-cart-color="${item.color}" data-delta="-1">-1</button>
              <button class="button button--secondary" type="button" data-cart-id="${product.id}" data-cart-size="${item.size}" data-cart-color="${item.color}" data-delta="1">+1</button>
            </div>
          </div>
          <strong>${formatCurrency(product.price * item.quantity)}</strong>
        </article>
      `;
    })
    .join("");

  subtotal.textContent = formatCurrency(cartSubtotal(cart));

  list.querySelectorAll("[data-cart-id]").forEach((button) => {
    button.addEventListener("click", () => {
      changeQuantity(
        button.dataset.cartId,
        button.dataset.cartSize || "",
        button.dataset.cartColor || "",
        Number(button.dataset.delta)
      );
    });
  });
}

function updatePaymentPanels(hasItems) {
  const methodButtons = [...document.querySelectorAll("[data-payment-method]")];
  const stripePanel = document.getElementById("stripePanel");
  const paypalPanel = document.getElementById("paypalPanel");
  const activeMethod = getActivePaymentMethod();

  if (!methodButtons.length || !stripePanel || !paypalPanel) {
    return;
  }

  methodButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.paymentMethod === activeMethod);
  });

  stripePanel.hidden = activeMethod !== "stripe";
  paypalPanel.hidden = activeMethod !== "paypal";

  const paypalHint = document.getElementById("paypalHint");
  const paypalLink = document.getElementById("paypalCheckoutLink");
  const paypalButton = document.getElementById("paypalCheckoutButton");
  const paypalConfigLink = (window.SHOP_CONFIG && window.SHOP_CONFIG.paypalCheckoutLink) || "";
  const paypalNotice = (window.SHOP_CONFIG && window.SHOP_CONFIG.paypalNotice) || "";

  if (!paypalHint || !paypalLink || !paypalButton) {
    return;
  }

  if (paypalConfigLink && hasItems) {
    paypalHint.textContent = "PayPal ist vorbereitet und kann mit einem echten Checkout-Link geöffnet werden.";
    paypalLink.hidden = false;
    paypalLink.href = paypalConfigLink;
    paypalButton.hidden = true;
    return;
  }

  paypalHint.textContent = hasItems
    ? paypalNotice
    : "Lege zuerst Produkte in den Demo-Warenkorb.";
  paypalLink.hidden = true;
  paypalButton.hidden = false;
  paypalButton.disabled = true;
}

function bindPaymentSwitcher() {
  const methodButtons = [...document.querySelectorAll("[data-payment-method]")];
  if (!methodButtons.length) {
    return;
  }

  methodButtons.forEach((button) => {
    button.addEventListener("click", () => {
      setActivePaymentMethod(button.dataset.paymentMethod || "stripe");
      updatePaymentPanels(readCart().length > 0);
    });
  });
}

function renderCheckout() {
  const list = document.getElementById("checkoutSummary");
  const total = document.getElementById("checkoutTotal");
  const stripeButton = document.getElementById("stripeCheckoutButton");
  const stripeHint = document.getElementById("stripeHint");

  if (!list || !total || !stripeButton || !stripeHint) {
    return;
  }

  const cart = readCart();
  const paymentLink = (window.SHOP_CONFIG && window.SHOP_CONFIG.stripePaymentLink) || "";
  const notice = (window.SHOP_CONFIG && window.SHOP_CONFIG.shopNotice) || "";
  const hasItems = cart.length > 0;

  if (!hasItems) {
    list.innerHTML = `<p class="cart-empty">Noch keine Produkte im Warenkorb. Gehe zur Shop-Demo und lege Beispielprodukte hinein.</p>`;
    total.textContent = formatCurrency(0);
  } else {
    list.innerHTML = cart
      .map((item) => {
        const product = getProduct(item.id);
        if (!product) {
          return "";
        }
        return `
          <div class="summary-line">
            <span>${product.title} (${getVariantLabel(item)}) x ${item.quantity}</span>
            <strong>${formatCurrency(product.price * item.quantity)}</strong>
          </div>
        `;
      })
      .join("");
    total.textContent = formatCurrency(cartSubtotal(cart));
  }

  if (paymentLink && hasItems) {
    stripeButton.disabled = false;
    stripeButton.textContent = "Weiter zu Stripe Checkout";
    stripeHint.textContent =
      "Die Demo ist vorbereitet und leitet mit einem echten Payment Link an Stripe weiter.";
    stripeButton.onclick = () => {
      window.location.href = paymentLink;
    };
  } else {
    stripeButton.disabled = true;
    stripeButton.textContent = hasItems ? "Stripe-Link fehlt" : "Warenkorb leer";
    stripeHint.textContent = hasItems ? notice : "Lege zuerst Produkte in den Demo-Warenkorb.";
    stripeButton.onclick = null;
  }

  updatePaymentPanels(hasItems);
}

function bindOverlays() {
  const productModalShell = document.getElementById("productModalShell");
  const cartDrawerShell = document.getElementById("cartDrawerShell");
  const openCartButton = document.getElementById("openCart");
  const closeCartButton = document.getElementById("closeCart");

  if (openCartButton && cartDrawerShell) {
    openCartButton.addEventListener("click", () => openElement(cartDrawerShell));
  }

  if (closeCartButton && cartDrawerShell) {
    closeCartButton.addEventListener("click", () => closeElement(cartDrawerShell));
  }

  [productModalShell, cartDrawerShell].forEach((shell) => {
    if (!shell) {
      return;
    }
    shell.addEventListener("click", (event) => {
      if (event.target === shell) {
        closeElement(shell);
      }
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") {
      return;
    }
    closeElement(productModalShell);
    closeElement(cartDrawerShell);
  });
}

function initShop() {
  renderShopProducts();
  renderRecommendedProducts();
  renderCart();
  bindPaymentSwitcher();
  renderCheckout();
  bindOverlays();
}

initShop();
