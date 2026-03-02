const searchInput = document.getElementById("portfolioSearch");
const portfolioGrid = document.getElementById("portfolioGrid");
const resultCount = document.getElementById("portfolioResultCount");
const emptyState = document.getElementById("portfolioEmptyState");
const chips = [...document.querySelectorAll("[data-filter]")];
const faqTriggers = [...document.querySelectorAll(".faq-trigger")];
const progressBar = document.getElementById("scrollProgress");
const navLinks = [...document.querySelectorAll(".site-nav__link")];
const announcementText = document.getElementById("announcementText");
const revealTargets = [...document.querySelectorAll("[data-reveal]")];
const countTargets = [...document.querySelectorAll("[data-count]")];

const announcements = [
  "Mehr Produkte, Social-Funnel und modernisierte Commerce-Landingpage sind live.",
  "Shop-Demo, KPI-Dashboard, Matchday-Funnel und CRM-Case bilden jetzt ein komplettes Portfolio.",
  "Suchfunktion, Filter, Motion und klarere Content-Struktur sorgen für einen stärkeren Shop-Auftritt."
];

let activeFilter = "all";
let announcementIndex = 0;

function normalize(text) {
  return (text || "")
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function runWithTransition(fn) {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!prefersReducedMotion && typeof document.startViewTransition === "function") {
    document.startViewTransition(fn);
    return;
  }
  fn();
}

function updateScrollProgress() {
  if (!progressBar) {
    return;
  }
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  const progress = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
  progressBar.style.width = `${progress}%`;
}

function filterPortfolio() {
  if (!searchInput || !portfolioGrid || !resultCount || !emptyState) {
    return;
  }

  const term = normalize(searchInput.value);
  const cards = [...portfolioGrid.querySelectorAll(".portfolio-card")];
  let matches = 0;

  cards.forEach((card) => {
    const category = card.dataset.category;
    const haystack = normalize(card.dataset.search || "");
    const categoryMatch = activeFilter === "all" || category === activeFilter;
    const textMatch = term === "" || haystack.includes(term);
    const visible = categoryMatch && textMatch;
    card.classList.toggle("is-hidden", !visible);

    if (visible) {
      matches += 1;
    }
  });

  resultCount.textContent = `${matches} Projekt${matches === 1 ? "" : "e"} gefunden`;
  emptyState.hidden = matches !== 0;
}

function bindFilterChips() {
  if (!chips.length) {
    return;
  }

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      runWithTransition(() => {
        activeFilter = chip.dataset.filter || "all";
        chips.forEach((button) => button.classList.toggle("is-active", button === chip));
        filterPortfolio();
      });
    });
  });
}

function bindFaq() {
  faqTriggers.forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const isOpen = trigger.getAttribute("aria-expanded") === "true";

      runWithTransition(() => {
        faqTriggers.forEach((button) => {
          button.setAttribute("aria-expanded", "false");
          button.nextElementSibling.hidden = true;
        });

        if (!isOpen) {
          trigger.setAttribute("aria-expanded", "true");
          trigger.nextElementSibling.hidden = false;
        }
      });
    });
  });
}

function bindKeyboardShortcuts() {
  window.addEventListener("keydown", (event) => {
    const typingTarget =
      event.target instanceof HTMLElement &&
      ["INPUT", "TEXTAREA"].includes(event.target.tagName);

    if (event.key === "/" && !typingTarget && searchInput) {
      event.preventDefault();
      searchInput.focus();
      searchInput.select();
    }
  });
}

function bindSectionHighlight() {
  const sections = [...document.querySelectorAll("[data-section]")];
  const targets = navLinks
    .map((link) => {
      const id = link.getAttribute("href");
      return { link, target: id ? document.querySelector(id) : null };
    })
    .filter((item) => item.target);

  if (!targets.length) {
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        const currentId = `#${entry.target.id}`;
        targets.forEach(({ link }) => {
          link.classList.toggle("is-active", link.getAttribute("href") === currentId);
        });
      });
    },
    { rootMargin: "-35% 0px -50% 0px", threshold: 0 }
  );

  sections.forEach((section) => observer.observe(section));
}

function startAnnouncementRotation() {
  if (!announcementText) {
    return;
  }

  window.setInterval(() => {
    announcementIndex = (announcementIndex + 1) % announcements.length;
    announcementText.textContent = announcements[announcementIndex];
  }, 3400);
}

function bindRevealObserver() {
  if (!revealTargets.length) {
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "0px 0px -12% 0px", threshold: 0.12 }
  );

  revealTargets.forEach((target) => observer.observe(target));
}

function animateCounter(element) {
  const target = Number(element.dataset.count);
  if (!Number.isFinite(target)) {
    return;
  }

  const duration = 900;
  const startTime = performance.now();

  function step(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    const value = Math.round(target * (1 - Math.pow(1 - progress, 3)));
    element.textContent = String(value);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  }

  window.requestAnimationFrame(step);
}

function bindCounters() {
  if (!countTargets.length) {
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        animateCounter(entry.target);
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.45 }
  );

  countTargets.forEach((target) => observer.observe(target));
}

if (searchInput) {
  searchInput.addEventListener("input", filterPortfolio);
}

window.addEventListener("scroll", updateScrollProgress, { passive: true });

bindFilterChips();
bindFaq();
bindKeyboardShortcuts();
bindSectionHighlight();
bindRevealObserver();
bindCounters();
startAnnouncementRotation();
updateScrollProgress();
filterPortfolio();
