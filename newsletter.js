const NEWSLETTER_STORAGE_KEY = "scf_newsletter_leads";

function readLeads() {
  try {
    const raw = JSON.parse(localStorage.getItem(NEWSLETTER_STORAGE_KEY) || "[]");
    return Array.isArray(raw) ? raw : [];
  } catch {
    return [];
  }
}

function writeLeads(leads) {
  localStorage.setItem(NEWSLETTER_STORAGE_KEY, JSON.stringify(leads));
}

function formatLeadDate(value) {
  try {
    return new Date(value).toLocaleDateString("de-DE", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric"
    });
  } catch {
    return value;
  }
}

function renderLeadState() {
  const countTarget = document.getElementById("newsletterCount");
  const listTarget = document.getElementById("audienceList");
  const leads = readLeads().slice().reverse();

  if (countTarget) {
    countTarget.textContent = String(leads.length);
  }

  if (listTarget) {
    if (!leads.length) {
      listTarget.innerHTML = `<p class="cart-empty">Noch keine Einträge gespeichert.</p>`;
      return;
    }

    listTarget.innerHTML = leads
      .slice(0, 5)
      .map(
        (lead) => `
          <div class="audience-entry">
            <div>
              <strong>${lead.name}</strong>
              <p>${lead.email}</p>
            </div>
            <span>${formatLeadDate(lead.createdAt)}</span>
          </div>
        `
      )
      .join("");
  }
}

function setStatus(message, type = "default") {
  const status = document.getElementById("newsletterStatus");
  if (!status) {
    return;
  }

  status.dataset.state = type;
  status.innerHTML = `<p>${message}</p>`;
}

function updatePreviewName(name) {
  const target = document.getElementById("welcomePreviewName");
  if (target) {
    target.textContent = name || "Max";
  }
}

async function loadEmailJs() {
  if (window.emailjs) {
    return window.emailjs;
  }

  await new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js";
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });

  return window.emailjs;
}

async function sendWelcomeEmail(entry) {
  const config = window.NEWSLETTER_CONFIG || {};
  const ready =
    config.emailjsPublicKey &&
    config.emailjsServiceId &&
    config.emailjsWelcomeTemplateId;

  if (!ready) {
    return { sent: false };
  }

  const emailjs = await loadEmailJs();
  emailjs.init({ publicKey: config.emailjsPublicKey });

  await emailjs.send(config.emailjsServiceId, config.emailjsWelcomeTemplateId, {
    subscriber_name: entry.name,
    subscriber_email: entry.email,
    subscriber_channel: entry.channel
  });

  if (config.emailjsOwnerTemplateId) {
    await emailjs.send(config.emailjsServiceId, config.emailjsOwnerTemplateId, {
      subscriber_name: entry.name,
      subscriber_email: entry.email,
      subscriber_channel: entry.channel,
      owner_email: config.ownerEmail || ""
    });
  }

  return { sent: true };
}

async function saveRemoteLead(entry) {
  const config = window.NEWSLETTER_CONFIG || {};
  if (!config.saveEndpoint) {
    return { saved: false };
  }

  const response = await fetch(config.saveEndpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(entry)
  });

  if (!response.ok) {
    throw new Error(`Save endpoint responded with ${response.status}`);
  }

  return { saved: true };
}

function bindNewsletterForm() {
  const form = document.getElementById("newsletterForm");
  if (!form) {
    return;
  }

  const nameInput = document.getElementById("newsletterName");
  const emailInput = document.getElementById("newsletterEmail");
  const channelInput = document.getElementById("newsletterChannel");
  const submitButton = document.getElementById("newsletterSubmit");

  nameInput?.addEventListener("input", () => updatePreviewName(nameInput.value.trim()));

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const name = nameInput?.value.trim() || "";
    const email = emailInput?.value.trim() || "";
    const channel = channelInput?.value || "Instagram";

    if (!name || !email) {
      setStatus("Bitte Name und E-Mail vollständig eintragen.", "error");
      return;
    }

    const leads = readLeads();
    if (leads.some((lead) => lead.email.toLowerCase() === email.toLowerCase())) {
      setStatus("Diese E-Mail ist in der Demo bereits gespeichert.", "warning");
      return;
    }

    const entry = {
      name,
      email,
      channel,
      createdAt: new Date().toISOString()
    };

    leads.push(entry);
    writeLeads(leads);
    renderLeadState();

    submitButton.disabled = true;
    setStatus("Lead wird gespeichert und Welcome-Mail vorbereitet ...");

    let remoteSaved = false;
    let welcomeSent = false;

    try {
      const [remoteResult, emailResult] = await Promise.allSettled([
        saveRemoteLead(entry),
        sendWelcomeEmail(entry)
      ]);

      if (remoteResult.status === "fulfilled") {
        remoteSaved = remoteResult.value.saved;
      }

      if (emailResult.status === "fulfilled") {
        welcomeSent = emailResult.value.sent;
      }

      const fallbackNote = (window.NEWSLETTER_CONFIG && window.NEWSLETTER_CONFIG.statusNote) || "";
      const parts = [`${name} wurde als neuer Lead erfasst.`];

      if (remoteSaved) {
        parts.push("Der Lead wurde an den externen Speicher weitergegeben.");
      }

      if (welcomeSent) {
        parts.push("Die Welcome-Mail wurde über EmailJS ausgelöst.");
      } else {
        parts.push(fallbackNote);
      }

      setStatus(parts.join(" "), "success");
      form.reset();
      updatePreviewName("");
    } catch (error) {
      setStatus(
        `Lead lokal gespeichert. Externe Automatisierung konnte nicht vollständig ausgeführt werden. ${error.message}`,
        "warning"
      );
    } finally {
      submitButton.disabled = false;
    }
  });
}

renderLeadState();
bindNewsletterForm();
