const projects = [
  {
    title: "Digital Brand Launch",
    subtitle: "Privates E-Commerce-Projekt",
    type: "Shop-Aufbau",
    role: "Konzept, Produktauswahl, Shop-Struktur, Angebotsseiten und Testing",
    description:
      "In diesem Projekt habe ich eine kleine digitale Brand von der Idee bis zur präsentierbaren Shop-Fläche aufgebaut. Der Fokus lag auf Produktpositionierung, klaren Angebotsseiten, einfachen Kaufanreizen und einem sauberen visuellen Auftritt.",
    image: "assets/brand-launch.svg",
    imageAlt: "Visualisierung eines privaten E-Commerce-Shop-Projekts",
    metrics: [
      { value: "D2C", label: "Ausrichtung auf direkte Verkäufe" },
      { value: "Shop", label: "Struktur mit Fokus auf Klarheit" },
      { value: "Tests", label: "Creatives und Angebotsvarianten geprüft" }
    ],
    focus: [
      "Produktideen und Zielgruppen logisch strukturieren",
      "Aufbau einer verständlichen Shop- und Landingpage-Logik",
      "Optimierung von Texten und visueller Produktpräsentation"
    ],
    learnings: [
      "Gute Produktseiten entscheiden stark über Vertrauen und Kaufinteresse",
      "Schon kleine Anpassungen an Hooks und Bildern verändern die Wirkung",
      "E-Commerce braucht sauberes Zusammenspiel aus Marke, Angebot und Daten"
    ]
  },
  {
    title: "Social Media Funnel",
    subtitle: "Privates Marketing-Projekt",
    type: "Performance & Content",
    role: "Content-Ideen, Creatives, Reichweitenaufbau und Kennzahlenbeobachtung",
    description:
      "Hier habe ich Social-Media-Inhalte mit Verkaufslogik verbunden. Ziel war es, Aufmerksamkeit aufzubauen, Interessenten auf Angebotsseiten zu lenken und aus Reaktionen konkrete Optimierungen für Botschaft, Creatives und Zielgruppenansprache abzuleiten.",
    image: "assets/social-funnel.svg",
    imageAlt: "Visualisierung eines Social-Media- und Marketing-Projekts",
    metrics: [
      { value: "Content", label: "Hook, Visual und Angebot verbunden" },
      { value: "Funnel", label: "Aufmerksamkeit bis Klick mitgedacht" },
      { value: "Daten", label: "Reaktionen und Performance ausgewertet" }
    ],
    focus: [
      "Entwicklung von Content-Ideen mit klarem Nutzenversprechen",
      "Beobachtung von Klickverhalten und Resonanz auf Creatives",
      "Anpassung von Ansprache, Struktur und Call-to-Action"
    ],
    learnings: [
      "Relevanz für die Zielgruppe ist wichtiger als reine Reichweite",
      "Daten helfen, Inhalte schneller und gezielter zu verbessern",
      "Marketing funktioniert am besten, wenn Angebot und Kommunikation zusammenpassen"
    ]
  }
];

const tabsContainer = document.getElementById("projectTabs");
const image = document.getElementById("projectImage");
const type = document.getElementById("projectType");
const title = document.getElementById("projectTitle");
const role = document.getElementById("projectRole");
const description = document.getElementById("projectDescription");
const metrics = document.getElementById("projectMetrics");
const focus = document.getElementById("projectFocus");
const learnings = document.getElementById("projectLearnings");
const prevButton = document.getElementById("prevProject");
const nextButton = document.getElementById("nextProject");
const visualPanel = document.querySelector(".portfolio__visual");
const contentPanel = document.querySelector(".portfolio__content");

let currentProject = 0;

function renderList(items, target) {
  target.innerHTML = "";

  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    target.appendChild(li);
  });
}

function renderMetrics(items) {
  metrics.innerHTML = "";

  items.forEach((item) => {
    const metric = document.createElement("article");
    metric.className = "metric";

    const value = document.createElement("span");
    value.className = "metric__value";
    value.textContent = item.value;

    const label = document.createElement("span");
    label.className = "metric__label";
    label.textContent = item.label;

    metric.append(value, label);
    metrics.appendChild(metric);
  });
}

function updateTabs() {
  [...tabsContainer.children].forEach((button, index) => {
    button.classList.toggle("is-active", index === currentProject);
    button.setAttribute("aria-pressed", index === currentProject ? "true" : "false");
  });
}

function renderProject(index) {
  const project = projects[index];

  currentProject = index;
  visualPanel.classList.remove("is-swapping");
  contentPanel.classList.remove("is-swapping");
  void visualPanel.offsetWidth;
  image.src = project.image;
  image.alt = project.imageAlt;
  type.textContent = project.type;
  title.textContent = project.title;
  role.textContent = project.role;
  description.textContent = project.description;

  renderMetrics(project.metrics);
  renderList(project.focus, focus);
  renderList(project.learnings, learnings);
  updateTabs();
  visualPanel.classList.add("is-swapping");
  contentPanel.classList.add("is-swapping");
}

function changeProject(direction) {
  const nextIndex = (currentProject + direction + projects.length) % projects.length;
  renderProject(nextIndex);
}

projects.forEach((project, index) => {
  const button = document.createElement("button");
  button.className = "portfolio__tab";
  button.type = "button";
  button.innerHTML = `
    <span class="portfolio__tab-title">${project.title}</span>
    <span class="portfolio__tab-subtitle">${project.subtitle}</span>
  `;
  button.addEventListener("click", () => renderProject(index));
  tabsContainer.appendChild(button);
});

prevButton.addEventListener("click", () => changeProject(-1));
nextButton.addEventListener("click", () => changeProject(1));

window.addEventListener("keydown", (event) => {
  if (event.key === "ArrowLeft") {
    changeProject(-1);
  }

  if (event.key === "ArrowRight") {
    changeProject(1);
  }
});

renderProject(0);
