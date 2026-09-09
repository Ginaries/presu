const moneySymbols = {
  ARS: "$",
  USD: "US$",
  EUR: "€",
};

const catalog = {
  "Web": [
    {
      name: "Página de presentación o venta",
      description: "Una sola página para presentar un negocio, servicio, producto o promoción. Incluye estructura visual, secciones principales, llamada a la acción y formulario o botón de contacto.",
      price: 220000,
      billing: "once",
    },
    {
      name: "Sitio institucional",
      description: "Web clásica para una empresa, profesional o emprendimiento. Incluye inicio, secciones de servicios o información, datos de contacto y adaptación a celular, tablet y computadora.",
      price: 420000,
      billing: "once",
    },
    {
      name: "Página adicional",
      description: "Cada página interna extra que se suma al sitio, por ejemplo: preguntas frecuentes, casos de éxito, equipo, galería, blog o detalle de un servicio.",
      price: 65000,
      billing: "once",
    },
    {
      name: "SEO inicial",
      description: "Ajustes básicos para que Google y redes entiendan mejor la web: títulos, descripciones, estructura ordenada, textos alternativos y configuración inicial de indexación.",
      price: 85000,
      billing: "once",
    },
    {
      name: "Carga de contenido",
      description: "Carga de textos, imágenes, logos, datos de contacto, servicios o productos que entregue el cliente. No incluye redacción completa desde cero salvo que se cotice aparte.",
      price: 90000,
      billing: "once",
    },
    {
      name: "Formulario de contacto",
      description: "Formulario para recibir consultas con nombre, email, teléfono y mensaje. Incluye validaciones básicas y envío de la consulta al email definido.",
      price: 55000,
      billing: "once",
    },
  ],
  "Apps": [
    {
      name: "Aplicación web base",
      description: "Sistema que funciona desde el navegador y permite hacer tareas, no solo mostrar información. Incluye navegación, vistas principales y lógica inicial del negocio.",
      price: 850000,
      billing: "once",
    },
    {
      name: "Pantalla adicional",
      description: "Cada vista o flujo extra dentro del sistema, por ejemplo: clientes, ventas, reportes, turnos, pedidos, detalle de registro o historial.",
      price: 110000,
      billing: "once",
    },
    {
      name: "Login y usuarios",
      description: "Ingreso con usuario y contraseña para proteger el sistema. Puede incluir usuarios, roles simples, cierre de sesión y recuperación o cambio de contraseña.",
      price: 220000,
      billing: "once",
    },
    {
      name: "Base de datos básica",
      description: "Guardado de información simple como clientes, productos, consultas, turnos o pedidos. Incluye estructura de datos y operaciones básicas para crear, ver, editar y eliminar.",
      price: 180000,
      billing: "once",
    },
    {
      name: "Base de datos avanzada",
      description: "Base de datos con relaciones, búsquedas, filtros, estados, historial, reportes o reglas especiales. Se usa cuando la información ya no es una lista simple.",
      price: 360000,
      billing: "once",
    },
    {
      name: "Panel administrativo",
      description: "Área privada para que el cliente gestione información sin depender del programador: cargar, editar o eliminar contenidos, productos, usuarios o registros.",
      price: 260000,
      billing: "once",
    },
  ],
  "Automatizaciones": [
    {
      name: "Automatización simple",
      description: "Una tarea que se ejecuta sola entre herramientas. Ejemplo: llega un formulario, se guarda en una planilla y se envía un email de aviso.",
      price: 180000,
      billing: "once",
    },
    {
      name: "Automatización avanzada",
      description: "Proceso automático con varios pasos, condiciones y validaciones. Ejemplo: si el pago está aprobado se envía un mensaje, si falta información se genera un aviso.",
      price: 380000,
      billing: "once",
    },
    {
      name: "Integración con API",
      description: "Conexión entre la web/app y otro sistema, como Mercado Pago, WhatsApp, Google Sheets, CRM, email marketing o una plataforma externa.",
      price: 160000,
      billing: "once",
    },
    {
      name: "Dashboard o reporte",
      description: "Pantalla para ver datos importantes del negocio: ventas, consultas, pedidos, estados, métricas, tablas o reportes exportables.",
      price: 240000,
      billing: "once",
    },
  ],
  "Ecommerce": [
    {
      name: "Tienda online base",
      description: "Web para vender productos o servicios online. Incluye catálogo, detalle de producto, carrito, inicio de compra y configuración inicial de la tienda.",
      price: 760000,
      billing: "once",
    },
    {
      name: "Carga de productos",
      description: "Alta inicial de productos con nombre, precio, descripción, fotos, categorías y variantes si corresponden, según la información entregada por el cliente.",
      price: 140000,
      billing: "once",
    },
    {
      name: "Medios de pago",
      description: "Configuración de medios de pago como Mercado Pago, transferencia u otra pasarela. Incluye conexión, ajustes básicos y prueba de funcionamiento.",
      price: 130000,
      billing: "once",
    },
    {
      name: "Envíos",
      description: "Configuración de formas de entrega: retiro en local, zonas, costos, reglas de envío o conexión con proveedor logístico si aplica.",
      price: 95000,
      billing: "once",
    },
  ],
  "Infraestructura": [
    {
      name: "Deploy en servidor y puesta en marcha",
      description: "Publicar la web/app para que quede online y funcionando. Incluye configuración final, variables, revisión de enlaces, pruebas básicas y verificación de acceso.",
      price: 90000,
      billing: "once",
    },
    {
      name: "Deploy avanzado en servidor",
      description: "Puesta online en servidor propio o VPS. Incluye entorno productivo, configuración técnica, SSL, variables, procesos y revisión de funcionamiento.",
      price: 180000,
      billing: "once",
    },
    {
      name: "Configuración de dominio y DNS",
      description: "Conectar un dominio comprado por el cliente o ya existente con la web/app. Incluye registros DNS, conexión con hosting/servidor, SSL y validación de acceso.",
      price: 45000,
      billing: "once",
    },
    {
      name: "Costo de dominio anual (proveedor)",
      description: "Costo estimado de compra o renovación del dominio. Es un costo externo y depende de la extensión y del proveedor; el cliente también puede pagarlo directamente.",
      price: 25000,
      billing: "once",
    },
    {
      name: "Gestión de compra/renovación de dominio",
      description: "Asesoramiento y gestión para comprar o renovar el dominio, más coordinación técnica. El costo del dominio se cobra aparte o lo paga directamente el cliente al proveedor.",
      price: 70000,
      billing: "once",
    },
    {
      name: "SSL y seguridad inicial",
      description: "Configuración para que la web abra con candado HTTPS. Incluye certificado SSL, redirecciones seguras y ajustes básicos de protección.",
      price: 55000,
      billing: "once",
    },
    {
      name: "Migración o publicación de sitio existente",
      description: "Pasar una web existente a un nuevo servidor o dejarla publicada correctamente. Incluye subida de archivos, revisión, ajustes y prueba final.",
      price: 95000,
      billing: "once",
    },
  ],
  "Mensual": [
    {
      name: "Mantenimiento básico",
      description: "Revisión mensual para que la web siga funcionando. Incluye actualizaciones simples, backups, monitoreo básico y soporte técnico menor.",
      price: 80000,
      billing: "monthly",
    },
    {
      name: "Mantenimiento pro",
      description: "Soporte mensual más completo. Incluye backups, monitoreo, actualizaciones, resolución de incidencias y pequeñas mejoras acordadas.",
      price: 160000,
      billing: "monthly",
    },
    {
      name: "Gestión liviana",
      description: "Cambios chicos durante el mes, como modificar textos, fotos, horarios, banners, enlaces o datos de contacto.",
      price: 120000,
      billing: "monthly",
    },
    {
      name: "Gestión completa",
      description: "Gestión activa del sitio o app durante el mes. Incluye publicaciones, cambios de contenido, mejoras menores, seguimiento y soporte operativo.",
      price: 260000,
      billing: "monthly",
    },
    {
      name: "Hosting básico mensual",
      description: "Costo mensual del lugar donde vive la web. Incluye alojamiento, SSL y soporte técnico básico según proveedor o servicio contratado.",
      price: 65000,
      billing: "monthly",
    },
  ],
};

const autoBase = {
  website: { label: "Sitio web institucional", title: "Desarrollo de sitio web", base: 360000, unit: 62000 },
  landing: { label: "Página de presentación o venta", title: "Desarrollo de página de presentación o venta", base: 220000, unit: 30000 },
  ecommerce: { label: "Tienda online", title: "Desarrollo de tienda online", base: 690000, unit: 75000 },
  webapp: { label: "Aplicación web", title: "Desarrollo de aplicación web", base: 820000, unit: 115000 },
  mobileapp: { label: "Aplicación móvil", title: "Desarrollo de aplicación móvil", base: 1150000, unit: 140000 },
  automation: { label: "Automatización", title: "Desarrollo de automatización", base: 230000, unit: 125000 },
};

const state = {
  currentQuoteId: null,
  currentClientId: null,
  currentQuoteNumber: null,
  mode: "Manual",
  catalogCategory: "Web",
  items: [],
  recurringItems: [],
  quotes: [],
  lastAutoItems: [],
  lastAutoRecurringItems: [],
};

const el = {};

document.addEventListener("DOMContentLoaded", () => {
  cacheElements();
  hydrateIssuerFields(issuerDefaults());
  bindEvents();
  renderCatalogTabs();
  renderCatalog();
  renderItems();
  updateMode();
  updateTotals();
  updateHeader();
  loadQuotes();
});

function cacheElements() {
  [
    "newQuoteButton",
    "quoteSearch",
    "refreshButton",
    "quoteList",
    "quoteNumberLabel",
    "screenTitle",
    "duplicateButton",
    "deleteButton",
    "printButton",
    "saveButton",
    "statusMessage",
    "issuerBrand",
    "issuerTagline",
    "issuerEmail",
    "issuerPhone",
    "issuerWebsite",
    "issuerLocation",
    "clientName",
    "clientCompany",
    "clientEmail",
    "clientPhone",
    "clientNotes",
    "quoteTitle",
    "projectType",
    "currency",
    "quoteStatus",
    "manualModeButton",
    "autoModeButton",
    "manualPanel",
    "autoPanel",
    "catalogTabs",
    "catalogGrid",
    "customName",
    "customQty",
    "customPrice",
    "customBilling",
    "addCustomButton",
    "autoKind",
    "autoUnits",
    "autoComplexity",
    "autoDatabase",
    "autoLaunch",
    "autoDomain",
    "autoHosting",
    "autoAdmin",
    "autoIntegrations",
    "autoContent",
    "autoUrgency",
    "autoMaintenance",
    "autoManagement",
    "generateAutoButton",
    "addAutoButton",
    "itemsBody",
    "recurringBody",
    "scope",
    "notes",
    "discount",
    "taxPercent",
    "subtotalValue",
    "discountValue",
    "taxValue",
    "totalValue",
    "monthlyValue",
    "terms",
    "printArea",
  ].forEach((id) => {
    el[id] = document.getElementById(id);
  });
}

function bindEvents() {
  el.newQuoteButton.addEventListener("click", newQuote);
  el.refreshButton.addEventListener("click", loadQuotes);
  el.quoteSearch.addEventListener("input", renderQuoteList);
  el.manualModeButton.addEventListener("click", () => setMode("Manual"));
  el.autoModeButton.addEventListener("click", () => setMode("Automático"));
  el.addCustomButton.addEventListener("click", addCustomItem);
  el.generateAutoButton.addEventListener("click", () => applyAutoQuote(false));
  el.addAutoButton.addEventListener("click", () => applyAutoQuote(true));
  el.saveButton.addEventListener("click", saveQuote);
  el.printButton.addEventListener("click", downloadPdf);
  el.deleteButton.addEventListener("click", deleteQuote);
  el.duplicateButton.addEventListener("click", duplicateQuote);

  [
    el.currency,
    el.discount,
    el.taxPercent,
    el.quoteTitle,
    el.projectType,
    el.quoteStatus,
    el.scope,
    el.notes,
    el.terms,
    el.clientName,
    el.clientCompany,
    el.clientEmail,
    el.clientPhone,
    el.clientNotes,
  ].forEach((input) => {
    input.addEventListener("input", () => {
      updateTotals();
      updateHeader();
    });
  });

  [
    el.issuerBrand,
    el.issuerTagline,
    el.issuerEmail,
    el.issuerPhone,
    el.issuerWebsite,
    el.issuerLocation,
  ].forEach((input) => {
    input.addEventListener("input", () => {
      saveIssuerDefaults();
      updateTotals();
      updateHeader();
    });
  });
  el.currency.addEventListener("change", renderItems);
}

function setStatus(message, type = "") {
  el.statusMessage.textContent = message;
  el.statusMessage.className = `status-row ${type}`.trim();
}

function setMode(mode) {
  state.mode = mode;
  updateMode();
}

function updateMode() {
  const manual = state.mode === "Manual";
  el.manualModeButton.classList.toggle("active", manual);
  el.autoModeButton.classList.toggle("active", !manual);
  el.manualPanel.classList.toggle("hidden", !manual);
  el.autoPanel.classList.toggle("hidden", manual);
}

function renderCatalogTabs() {
  el.catalogTabs.innerHTML = "";
  Object.keys(catalog).forEach((category) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = category;
    button.className = category === state.catalogCategory ? "active" : "";
    button.addEventListener("click", () => {
      state.catalogCategory = category;
      renderCatalogTabs();
      renderCatalog();
    });
    el.catalogTabs.appendChild(button);
  });
}

function renderCatalog() {
  el.catalogGrid.innerHTML = "";
  catalog[state.catalogCategory].forEach((service) => {
    const tile = document.createElement("article");
    tile.className = "service-tile";
    tile.innerHTML = `
      <strong>${escapeHtml(service.name)}</strong>
      <p>${escapeHtml(service.description)}</p>
      <div class="tile-footer">
        <input type="number" min="0" step="1000" value="${service.price}" aria-label="Precio de ${escapeHtml(service.name)}">
        <button type="button">Agregar</button>
      </div>
    `;
    const priceInput = tile.querySelector("input");
    tile.querySelector("button").addEventListener("click", () => {
      addItem({
        name: service.name,
        description: service.description,
        qty: 1,
        unit_price: Number(priceInput.value) || 0,
        billing: service.billing,
      });
    });
    el.catalogGrid.appendChild(tile);
  });
}

function addCustomItem() {
  const name = el.customName.value.trim();
  if (!name) {
    setStatus("Escribí el nombre del servicio personalizado.", "error");
    return;
  }
  addItem({
    name,
    description: "Servicio definido a medida para este presupuesto.",
    qty: Number(el.customQty.value) || 1,
    unit_price: Number(el.customPrice.value) || 0,
    billing: el.customBilling.value,
  });
  el.customName.value = "";
  el.customQty.value = "1";
  el.customPrice.value = "";
}

function addItem(item) {
  const normalized = {
    id: crypto.randomUUID(),
    name: item.name,
    description: item.description || "",
    qty: Number(item.qty) || 1,
    unit_price: Number(item.unit_price) || 0,
  };
  if (item.billing === "monthly") {
    state.recurringItems.push(normalized);
  } else {
    state.items.push(normalized);
  }
  renderItems();
  updateTotals();
  setStatus(`Agregado: ${item.name}`, "success");
}

function renderItems() {
  renderItemTable(el.itemsBody, state.items, "once");
  renderItemTable(el.recurringBody, state.recurringItems, "monthly");
}

function renderItemTable(tbody, items, billing) {
  tbody.innerHTML = "";
  if (!items.length) {
    const row = document.createElement("tr");
    row.innerHTML = `<td colspan="6" class="empty-state">Sin ítems ${billing === "monthly" ? "mensuales" : "cargados"}.</td>`;
    tbody.appendChild(row);
    return;
  }

  items.forEach((item) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><input value="${escapeAttribute(item.name)}" aria-label="Concepto"></td>
      <td><textarea aria-label="Detalle">${escapeHtml(item.description)}</textarea></td>
      <td><input type="number" min="0" step="1" value="${item.qty}" aria-label="Cantidad"></td>
      <td><input type="number" min="0" step="1000" value="${item.unit_price}" aria-label="Precio unitario"></td>
      <td><span class="row-total">${formatMoney(item.qty * item.unit_price)}</span></td>
      <td><button class="remove-row" type="button" title="Quitar">×</button></td>
    `;
    const [nameInput, descriptionInput, qtyInput, priceInput] = row.querySelectorAll("input, textarea");
    nameInput.addEventListener("input", () => {
      item.name = nameInput.value;
      updatePrintOnly();
    });
    descriptionInput.addEventListener("input", () => {
      item.description = descriptionInput.value;
      updatePrintOnly();
    });
    qtyInput.addEventListener("input", () => {
      item.qty = Number(qtyInput.value) || 0;
      row.querySelector(".row-total").textContent = formatMoney(item.qty * item.unit_price);
      updateTotals();
    });
    priceInput.addEventListener("input", () => {
      item.unit_price = Number(priceInput.value) || 0;
      row.querySelector(".row-total").textContent = formatMoney(item.qty * item.unit_price);
      updateTotals();
    });
    row.querySelector("button").addEventListener("click", () => {
      const collection = billing === "monthly" ? state.recurringItems : state.items;
      const index = collection.findIndex((entry) => entry.id === item.id);
      if (index >= 0) {
        collection.splice(index, 1);
      }
      renderItems();
      updateTotals();
    });
    tbody.appendChild(row);
  });
}

function buildAutoItems() {
  const kind = el.autoKind.value;
  const base = autoBase[kind];
  const units = Math.max(1, Number(el.autoUnits.value) || 1);
  const complexity = el.autoComplexity.value;
  const database = el.autoDatabase.value;
  const launch = el.autoLaunch.value;
  const domain = el.autoDomain.value;
  const hosting = el.autoHosting.value;
  const admin = el.autoAdmin.value;
  const integrations = Number(el.autoIntegrations.value) || 0;
  const content = el.autoContent.value;
  const urgency = el.autoUrgency.value;
  const maintenance = el.autoMaintenance.value;
  const management = el.autoManagement.value;
  const complexityMultiplier = { simple: 0.85, medium: 1, advanced: 1.35 }[complexity];
  const generated = [];
  const monthly = [];
  const extraUnits = Math.max(0, units - 1);

  generated.push({
    id: crypto.randomUUID(),
    name: base.label,
    description: `Desarrollo principal del proyecto con complejidad ${complexityLabel(complexity).toLowerCase()}. Incluye estructura base, armado visual, adaptación a celular y computadora, lógica principal y revisión funcional inicial.`,
    qty: 1,
    unit_price: roundPrice(base.base * complexityMultiplier),
  });

  if (extraUnits > 0) {
    generated.push({
      id: crypto.randomUUID(),
      name: kind === "automation" ? "Flujos adicionales" : "Páginas o pantallas adicionales",
      description: `${extraUnits} unidad/es extra dentro del alcance. Puede representar secciones, pantallas internas, páginas de contenido o pasos adicionales del proceso.`,
      qty: extraUnits,
      unit_price: roundPrice(base.unit * complexityMultiplier),
    });
  }

  if (database !== "none") {
    generated.push({
      id: crypto.randomUUID(),
      name: database === "basic" ? "Base de datos básica" : "Base de datos avanzada",
      description: database === "basic"
        ? "Guardado de información simple como clientes, productos, consultas, turnos o pedidos. Incluye estructura de datos y operaciones básicas para crear, ver, editar y eliminar."
        : "Base de datos con relaciones, búsquedas, filtros, estados, historial, reportes o reglas especiales. Se usa cuando la información ya no es una lista simple.",
      qty: 1,
      unit_price: database === "basic" ? 180000 : 360000,
    });
  }

  if (launch !== "none") {
    generated.push({
      id: crypto.randomUUID(),
      name: launch === "standard" ? "Deploy en servidor y puesta en marcha" : "Deploy avanzado en servidor",
      description: launch === "standard"
        ? "Publicar la web/app para que quede online y funcionando. Incluye configuración final, variables necesarias, revisión de enlaces, pruebas básicas y verificación de acceso."
        : "Puesta online en servidor propio o VPS. Incluye entorno productivo, configuración técnica, SSL, variables, procesos y revisión de funcionamiento.",
      qty: 1,
      unit_price: launch === "standard" ? 90000 : 180000,
    });
  }

  if (domain !== "none") {
    const domainDetails = {
      existing: {
        name: "Configuración de dominio y DNS",
        description: "Conectar un dominio que el cliente ya tiene comprado con la web/app. Incluye registros DNS, conexión con hosting/servidor, SSL y validación de acceso.",
        price: 45000,
      },
      client: {
        name: "Configuración de dominio comprado por el cliente",
        description: "El cliente se hace cargo de comprar o renovar el dominio con el proveedor que prefiera. En este presupuesto se cobra solo la configuración: DNS, conexión con hosting/servidor, SSL y prueba de acceso.",
        price: 45000,
      },
      managed: {
        name: "Gestión de compra/renovación de dominio",
        description: "Asesoramiento y gestión para comprar o renovar el dominio, más configuración técnica. El costo del dominio es externo, depende del proveedor/extensión y puede ajustarse o pagarlo directamente el cliente.",
        price: 70000,
      },
    }[domain];

    generated.push({
      id: crypto.randomUUID(),
      name: domainDetails.name,
      description: domainDetails.description,
      qty: 1,
      unit_price: domainDetails.price,
    });
  }

  if (admin !== "none") {
    generated.push({
      id: crypto.randomUUID(),
      name: admin === "basic" ? "Panel de gestión simple" : "Panel de gestión avanzado",
      description: admin === "basic"
        ? "Área privada para que el cliente cargue, edite o elimine contenidos o registros principales sin tocar código."
        : "Área privada más completa con roles, filtros, estados, reportes internos y gestión de información más compleja.",
      qty: 1,
      unit_price: admin === "basic" ? 220000 : 420000,
    });
  }

  if (integrations > 0) {
    generated.push({
      id: crypto.randomUUID(),
      name: "Integraciones externas",
      description: "Conexión entre la web/app y otros sistemas, como Mercado Pago, WhatsApp, Google Sheets, CRM, email marketing o plataformas externas.",
      qty: integrations,
      unit_price: 155000,
    });
  }

  if (content !== "none") {
    generated.push({
      id: crypto.randomUUID(),
      name: content === "basic" ? "Carga básica de contenido" : "Carga completa de contenido",
      description: content === "basic"
        ? "Carga inicial de textos, imágenes, logos y datos provistos por el cliente. No incluye redacción completa desde cero salvo que se cotice aparte."
        : "Carga integral de contenido, productos o secciones principales con el material entregado por el cliente y ajustes de presentación.",
      qty: 1,
      unit_price: content === "basic" ? 90000 : 190000,
    });
  }

  if (urgency === "fast") {
    const subtotal = generated.reduce((sum, item) => sum + item.qty * item.unit_price, 0);
    generated.push({
      id: crypto.randomUUID(),
      name: "Prioridad de entrega",
      description: "Organización prioritaria del trabajo para acelerar tiempos de entrega. Incluye planificación especial y mayor disponibilidad durante el proyecto.",
      qty: 1,
      unit_price: roundPrice(subtotal * 0.18),
    });
  }

  if (maintenance !== "none") {
    monthly.push({
      id: crypto.randomUUID(),
      name: maintenance === "basic" ? "Mantenimiento básico" : "Mantenimiento pro",
      description: maintenance === "basic"
        ? "Revisión mensual para que la web siga funcionando. Incluye actualizaciones simples, backups, monitoreo básico y soporte técnico menor."
        : "Soporte mensual más completo. Incluye backups, monitoreo, actualizaciones, resolución de incidencias y pequeñas mejoras acordadas.",
      qty: 1,
      unit_price: maintenance === "basic" ? 80000 : 160000,
    });
  }

  if (hosting !== "none") {
    monthly.push({
      id: crypto.randomUUID(),
      name: hosting === "basic" ? "Hosting básico mensual" : "Servidor administrado mensual",
      description: hosting === "basic"
        ? "Costo mensual del lugar donde vive la web. Incluye alojamiento, SSL y soporte técnico básico según proveedor o servicio contratado."
        : "Servidor administrado para proyectos más complejos. Incluye monitoreo, SSL, backups técnicos, soporte mensual y administración básica del entorno.",
      qty: 1,
      unit_price: hosting === "basic" ? 65000 : 140000,
    });
  }

  if (management !== "none") {
    monthly.push({
      id: crypto.randomUUID(),
      name: management === "light" ? "Gestión mensual liviana" : "Gestión mensual completa",
      description: management === "light"
        ? "Cambios chicos durante el mes, como modificar textos, fotos, horarios, banners, enlaces o datos de contacto."
        : "Gestión activa del sitio o app durante el mes. Incluye publicaciones, cambios de contenido, mejoras menores, seguimiento y soporte operativo.",
      qty: 1,
      unit_price: management === "light" ? 120000 : 260000,
    });
  }

  state.lastAutoItems = generated;
  state.lastAutoRecurringItems = monthly;
  return { generated, monthly };
}

function applyAutoQuote(append) {
  const { generated, monthly } = buildAutoItems();
  const cloneItems = generated.map(cloneItem);
  const cloneMonthly = monthly.map(cloneItem);

  if (append) {
    state.items.push(...cloneItems);
    state.recurringItems.push(...cloneMonthly);
  } else {
    state.items = cloneItems;
    state.recurringItems = cloneMonthly;
  }

  const base = autoBase[el.autoKind.value];
  el.quoteTitle.value = base.title;
  el.projectType.value = {
    website: "Sitio web",
    landing: "Página de presentación o venta",
    ecommerce: "Tienda online",
    webapp: "Aplicación web",
    mobileapp: "Aplicación móvil",
    automation: "Automatización",
  }[el.autoKind.value];
  setMode("Automático");
  renderItems();
  updateTotals();
  updateHeader();
  setStatus(append ? "Se sumó el armado automático al presupuesto." : "Presupuesto automático armado.", "success");
}

function cloneItem(item) {
  return {
    ...item,
    id: crypto.randomUUID(),
  };
}

function complexityLabel(value) {
  return { simple: "Simple", medium: "Media", advanced: "Avanzada" }[value] || "Media";
}

function roundPrice(value) {
  return Math.round(value / 1000) * 1000;
}

function totals() {
  const subtotal = state.items.reduce((sum, item) => sum + item.qty * item.unit_price, 0);
  const discount = Math.min(Number(el.discount.value) || 0, subtotal);
  const taxable = Math.max(0, subtotal - discount);
  const taxPercent = Math.max(0, Number(el.taxPercent.value) || 0);
  const tax = taxable * (taxPercent / 100);
  const total = taxable + tax;
  const monthly_total = state.recurringItems.reduce((sum, item) => sum + item.qty * item.unit_price, 0);
  return { subtotal, discount, tax, total, monthly_total };
}

function updateTotals() {
  const current = totals();
  el.subtotalValue.textContent = formatMoney(current.subtotal);
  el.discountValue.textContent = formatMoney(current.discount);
  el.taxValue.textContent = formatMoney(current.tax);
  el.totalValue.textContent = formatMoney(current.total);
  el.monthlyValue.textContent = formatMoney(current.monthly_total);
  updatePrintOnly();
}

function updatePrintOnly() {
  buildPrintArea();
}

function updateHeader() {
  el.screenTitle.textContent = el.quoteTitle.value.trim() || "Armar presupuesto";
  el.quoteNumberLabel.textContent = state.currentQuoteNumber || "Nueva cotización";
  el.deleteButton.disabled = !state.currentQuoteId;
  el.duplicateButton.disabled = !state.currentQuoteId;
}

function quotePayload() {
  const current = totals();
  return {
    client: {
      id: state.currentClientId,
      name: el.clientName.value.trim(),
      company: el.clientCompany.value.trim(),
      email: el.clientEmail.value.trim(),
      phone: el.clientPhone.value.trim(),
      notes: el.clientNotes.value.trim(),
    },
    quote: {
      id: state.currentQuoteId,
      title: el.quoteTitle.value.trim() || "Presupuesto web",
      project_type: el.projectType.value,
      mode: state.mode,
      currency: el.currency.value,
      status: el.quoteStatus.value,
      scope: el.scope.value.trim(),
      notes: el.notes.value.trim(),
      terms: el.terms.value.trim(),
      config: autoConfig(),
      items: state.items,
      recurring_items: state.recurringItems,
      subtotal: current.subtotal,
      discount: current.discount,
      tax: current.tax,
      total: current.total,
      monthly_total: current.monthly_total,
    },
  };
}

function autoConfig() {
  return {
    kind: el.autoKind.value,
    units: Number(el.autoUnits.value) || 1,
    complexity: el.autoComplexity.value,
    database: el.autoDatabase.value,
    launch: el.autoLaunch.value,
    domain: el.autoDomain.value,
    hosting: el.autoHosting.value,
    admin: el.autoAdmin.value,
    integrations: Number(el.autoIntegrations.value) || 0,
    content: el.autoContent.value,
    urgency: el.autoUrgency.value,
    maintenance: el.autoMaintenance.value,
    management: el.autoManagement.value,
    tax_percent: Number(el.taxPercent.value) || 0,
    issuer: issuerData(),
  };
}

async function saveQuote() {
  if (!el.clientName.value.trim()) {
    setStatus("Para guardar, primero cargá el nombre del cliente.", "error");
    el.clientName.focus();
    return;
  }
  if (!state.items.length && !state.recurringItems.length) {
    setStatus("Agregá al menos un servicio antes de guardar.", "error");
    return;
  }

  try {
    const saved = await api("/api/quotes", {
      method: "POST",
      body: JSON.stringify(quotePayload()),
    });
    hydrateQuote(saved);
    await loadQuotes(false);
    setStatus(`Cotización ${saved.number} guardada en la base de datos.`, "success");
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function loadQuotes(showMessage = true) {
  try {
    state.quotes = await api("/api/quotes");
    renderQuoteList();
    if (showMessage) {
      setStatus("Cotizaciones actualizadas.", "success");
    }
  } catch (error) {
    setStatus(error.message, "error");
  }
}

function renderQuoteList() {
  const query = el.quoteSearch.value.trim().toLowerCase();
  const filtered = state.quotes.filter((quote) => {
    const haystack = [
      quote.number,
      quote.title,
      quote.project_type,
      quote.client_name,
      quote.client_company,
      quote.status,
    ].join(" ").toLowerCase();
    return haystack.includes(query);
  });

  el.quoteList.innerHTML = "";
  if (!filtered.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = state.quotes.length ? "No hay resultados para esa búsqueda." : "Todavía no hay cotizaciones guardadas.";
    el.quoteList.appendChild(empty);
    return;
  }

  filtered.forEach((quote) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `quote-card ${quote.id === state.currentQuoteId ? "active" : ""}`;
    button.innerHTML = `
      <strong>${escapeHtml(quote.client_name || "Cliente")}</strong>
      <span>${escapeHtml(quote.title)}</span>
      <div class="quote-meta">
        <span>${escapeHtml(quote.number)}</span>
        <span>${formatMoney(quote.total, quote.currency)}</span>
      </div>
      <div class="quote-meta">
        <span>${escapeHtml(quote.status)}</span>
        <span>${formatDate(quote.updated_at)}</span>
      </div>
    `;
    button.addEventListener("click", () => openQuote(quote.id));
    el.quoteList.appendChild(button);
  });
}

async function openQuote(id) {
  try {
    const quote = await api(`/api/quotes/${id}`);
    hydrateQuote(quote);
    setStatus(`Cotización ${quote.number} cargada.`, "success");
  } catch (error) {
    setStatus(error.message, "error");
  }
}

function hydrateQuote(quote) {
  state.currentQuoteId = quote.id;
  state.currentClientId = quote.client_id;
  state.currentQuoteNumber = quote.number;
  state.mode = quote.mode || "Manual";
  state.items = (quote.items || []).map(ensureItem);
  state.recurringItems = (quote.recurring_items || []).map(ensureItem);

  el.clientName.value = quote.client?.name || "";
  el.clientCompany.value = quote.client?.company || "";
  el.clientEmail.value = quote.client?.email || "";
  el.clientPhone.value = quote.client?.phone || "";
  el.clientNotes.value = quote.client?.notes || "";
  el.quoteTitle.value = quote.title || "";
  el.projectType.value = quote.project_type === "Landing page"
    ? "Página de presentación o venta"
    : quote.project_type || "Sitio web";
  el.currency.value = quote.currency || "ARS";
  el.quoteStatus.value = quote.status || "Borrador";
  el.scope.value = quote.scope || "";
  el.notes.value = quote.notes || "";
  el.terms.value = quote.terms || "";
  el.discount.value = quote.discount || 0;
  const taxable = Math.max(0, (quote.subtotal || 0) - (quote.discount || 0));
  el.taxPercent.value = taxable ? roundNumber(((quote.tax || 0) / taxable) * 100, 2) : 0;
  hydrateAutoConfig(quote.config || {});

  renderItems();
  updateMode();
  updateTotals();
  updateHeader();
  renderQuoteList();
}

function hydrateAutoConfig(config) {
  const domain = {
    dns: "existing",
    annual: "managed",
  }[config.domain] || config.domain || "none";
  const issuer = config.issuer || issuerDefaults();

  el.autoKind.value = config.kind || "website";
  el.autoUnits.value = config.units || 5;
  el.autoComplexity.value = config.complexity || "medium";
  el.autoDatabase.value = config.database || "none";
  el.autoLaunch.value = config.launch || "none";
  el.autoDomain.value = domain;
  el.autoHosting.value = config.hosting || "none";
  el.autoAdmin.value = config.admin || "none";
  el.autoIntegrations.value = String(config.integrations ?? 0);
  el.autoContent.value = config.content || "none";
  el.autoUrgency.value = config.urgency || "normal";
  el.autoMaintenance.value = config.maintenance || "none";
  el.autoManagement.value = config.management || "none";
  el.issuerBrand.value = issuer.brand || "";
  el.issuerTagline.value = issuer.tagline || "";
  el.issuerEmail.value = issuer.email || "";
  el.issuerPhone.value = issuer.phone || "";
  el.issuerWebsite.value = issuer.website || "";
  el.issuerLocation.value = issuer.location || "";
}

function ensureItem(item) {
  return {
    id: item.id || crypto.randomUUID(),
    name: item.name || "Servicio",
    description: item.description || "",
    qty: Number(item.qty) || 1,
    unit_price: Number(item.unit_price) || 0,
  };
}

function newQuote() {
  state.currentQuoteId = null;
  state.currentClientId = null;
  state.currentQuoteNumber = null;
  state.mode = "Manual";
  state.items = [];
  state.recurringItems = [];
  el.clientName.value = "";
  el.clientCompany.value = "";
  el.clientEmail.value = "";
  el.clientPhone.value = "";
  el.clientNotes.value = "";
  hydrateIssuerFields(issuerDefaults());
  el.quoteTitle.value = "Desarrollo de sitio web";
  el.projectType.value = "Sitio web";
  el.currency.value = "ARS";
  el.quoteStatus.value = "Borrador";
  el.scope.value = "Diseño responsive, desarrollo y configuración inicial según el alcance detallado. La puesta online, dominio, hosting y mantenimiento se incluyen solo si figuran como ítems del presupuesto.";
  el.notes.value = "";
  el.terms.value = "Validez del presupuesto: 15 días. Forma de pago sugerida: 50% para iniciar y 50% contra entrega.";
  el.discount.value = "0";
  el.taxPercent.value = "0";
  hydrateAutoConfig({});
  renderItems();
  updateMode();
  updateTotals();
  updateHeader();
  renderQuoteList();
  setStatus("Nueva cotización lista.", "success");
}

async function deleteQuote() {
  if (!state.currentQuoteId) {
    return;
  }
  const confirmed = confirm(`¿Eliminar la cotización ${state.currentQuoteNumber}?`);
  if (!confirmed) {
    return;
  }
  try {
    await api(`/api/quotes/${state.currentQuoteId}`, { method: "DELETE" });
    newQuote();
    await loadQuotes(false);
    setStatus("Cotización eliminada.", "success");
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function duplicateQuote() {
  if (!state.currentQuoteId) {
    return;
  }
  try {
    const copy = await api(`/api/quotes/${state.currentQuoteId}/duplicate`, { method: "POST" });
    hydrateQuote(copy);
    await loadQuotes(false);
    setStatus(`Se creó la copia ${copy.number}.`, "success");
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function downloadPdf() {
  if (!state.items.length && !state.recurringItems.length) {
    setStatus("Agregá servicios antes de exportar a PDF.", "error");
    return;
  }
  const payload = quotePayload();
  payload.quote.number = state.currentQuoteNumber || "presupuesto";

  try {
    setStatus("Generando PDF...", "");
    const response = await fetch("/api/pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.error || "No se pudo generar el PDF.");
    }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${safeFileName(payload.quote.number || payload.quote.title)}.pdf`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    setStatus("PDF descargado sin pie de localhost.", "success");
  } catch (error) {
    setStatus(`${error.message} Usá la impresión del navegador como respaldo.`, "error");
    buildPrintArea();
  }
}

function printQuote() {
  if (!state.items.length && !state.recurringItems.length) {
    setStatus("Agregá servicios antes de exportar a PDF.", "error");
    return;
  }
  buildPrintArea();
  window.print();
}

function buildPrintArea() {
  const current = totals();
  const issuer = issuerData();
  const clientLines = [
    el.clientCompany.value.trim(),
    el.clientName.value.trim(),
    el.clientEmail.value.trim(),
    el.clientPhone.value.trim(),
  ].filter(Boolean);
  const quoteNumber = state.currentQuoteNumber || "Sin guardar";
  const issueDate = new Date().toLocaleDateString("es-AR", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });
  const servicesCount = state.items.length + state.recurringItems.length;
  const issuerLines = [
    issuer.email,
    issuer.phone,
    issuer.website,
    issuer.location,
  ].filter(Boolean);
  const clientName = el.clientCompany.value.trim() || el.clientName.value.trim() || "Cliente";
  el.printArea.innerHTML = `
    <article class="print-document">
      <header class="print-header">
        <div class="print-brand">
          <div class="print-mark">${escapeHtml(initials(issuer.brand || "PW"))}</div>
          <div>
            <strong>${escapeHtml(issuer.brand || "Presupuestos Web")}</strong>
            <span>${escapeHtml(issuer.tagline || "Desarrollo web, apps y automatizaciones")}</span>
          </div>
        </div>
        <div class="print-doc-meta">
          <span>${escapeHtml(quoteNumber)}</span>
          <strong>${escapeHtml(el.quoteStatus.value)}</strong>
          <span>${issueDate}</span>
        </div>
      </header>

      <section class="print-hero">
        <div>
          <span>Propuesta comercial</span>
          <h1>${escapeHtml(el.quoteTitle.value || "Presupuesto")}</h1>
          <p>Preparada para <strong>${escapeHtml(clientName)}</strong></p>
        </div>
        <div class="print-investment">
          <span>Inversión estimada</span>
          <strong>${formatMoney(current.total)}</strong>
          ${current.monthly_total ? `<small>+ ${formatMoney(current.monthly_total)} mensuales</small>` : "<small>Sin abono mensual incluido</small>"}
        </div>
      </section>

      <section class="print-summary">
        <div>
          <span>Tipo de proyecto</span>
          <strong>${escapeHtml(el.projectType.value)}</strong>
        </div>
        <div>
          <span>Servicios cotizados</span>
          <strong>${servicesCount}</strong>
        </div>
        <div>
          <span>Moneda</span>
          <strong>${escapeHtml(el.currency.value)}</strong>
        </div>
        <div>
          <span>Validez</span>
          <strong>${escapeHtml(validityLabel())}</strong>
        </div>
      </section>

      <section class="print-parties">
        <div>
          <h2>Cliente</h2>
          ${clientLines.map((line) => `<p>${escapeHtml(line)}</p>`).join("") || "<p>Sin cliente asignado</p>"}
        </div>
        <div>
          <h2>Emitido por</h2>
          <p><strong>${escapeHtml(issuer.brand || "Presupuestos Web")}</strong></p>
          ${issuerLines.map((line) => `<p>${escapeHtml(line)}</p>`).join("")}
        </div>
      </section>

      <section class="print-block print-scope">
        <h2>Alcance</h2>
        <p>${nl2br(escapeHtml(el.scope.value || "Según detalle de servicios."))}</p>
      </section>

      ${printTable("Detalle del proyecto", state.items, "unitario")}
      ${state.recurringItems.length ? printTable("Servicios mensuales", state.recurringItems, "mensual") : ""}

      <section class="print-block print-totals-block">
        <div>
          <h2>Resumen económico</h2>
          <p>Los valores se calculan según los conceptos detallados en esta propuesta.</p>
        </div>
        <div class="print-totals">
          <div><span>Subtotal</span><strong>${formatMoney(current.subtotal)}</strong></div>
          <div><span>Descuento</span><strong>${formatMoney(current.discount)}</strong></div>
          <div><span>Impuestos</span><strong>${formatMoney(current.tax)}</strong></div>
          <div class="grand"><span>Total proyecto</span><strong>${formatMoney(current.total)}</strong></div>
          ${current.monthly_total ? `<div><span>Total mensual</span><strong>${formatMoney(current.monthly_total)}</strong></div>` : ""}
        </div>
      </section>

      ${el.notes.value.trim() ? `<section class="print-block"><h2>Notas</h2><p>${nl2br(escapeHtml(el.notes.value))}</p></section>` : ""}
      ${el.terms.value.trim() ? `<section class="print-block"><h2>Condiciones</h2><p>${nl2br(escapeHtml(el.terms.value))}</p></section>` : ""}
      <footer class="print-footer">
        <span>${escapeHtml(issuer.brand || "Presupuestos Web")}</span>
        <span>${escapeHtml(quoteNumber)}</span>
      </footer>
    </article>
  `;
}

function printTable(title, items, label) {
  if (!items.length) {
    return "";
  }
  return `
    <section class="print-block">
      <h2>${escapeHtml(title)}</h2>
      <table class="print-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Concepto</th>
            <th>Detalle</th>
            <th>Cant.</th>
            <th>${label === "mensual" ? "Mensual" : "Unitario"}</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          ${items.map((item, index) => `
            <tr>
              <td>${index + 1}</td>
              <td>${escapeHtml(item.name)}</td>
              <td>${escapeHtml(item.description)}</td>
              <td>${item.qty}</td>
              <td>${formatMoney(item.unit_price)}</td>
              <td>${formatMoney(item.qty * item.unit_price)}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </section>
  `;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || "No se pudo completar la operación.");
  }
  return data;
}

function formatMoney(value, currency = el.currency?.value || "ARS") {
  const symbol = moneySymbols[currency] || "$";
  return `${symbol} ${Number(value || 0).toLocaleString("es-AR", {
    maximumFractionDigits: 0,
  })}`;
}

function formatDate(value) {
  if (!value) {
    return "";
  }
  return new Date(value).toLocaleDateString("es-AR");
}

function roundNumber(value, digits) {
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value);
}

function nl2br(value) {
  return value.replaceAll("\n", "<br>");
}

function validityLabel() {
  const terms = el.terms.value || "";
  const match = terms.match(/validez[^0-9]*(\d+)\s*d[ií]as?/i) || terms.match(/(\d+)\s*d[ií]as?/i);
  return match ? `${match[1]} días` : "Ver condiciones";
}

function issuerData() {
  return {
    brand: el.issuerBrand?.value.trim() || "",
    tagline: el.issuerTagline?.value.trim() || "",
    email: el.issuerEmail?.value.trim() || "",
    phone: el.issuerPhone?.value.trim() || "",
    website: el.issuerWebsite?.value.trim() || "",
    location: el.issuerLocation?.value.trim() || "",
  };
}

function issuerDefaults() {
  try {
    return JSON.parse(localStorage.getItem("budgetIssuerDefaults") || "{}");
  } catch {
    return {};
  }
}

function hydrateIssuerFields(issuer) {
  el.issuerBrand.value = issuer.brand || "";
  el.issuerTagline.value = issuer.tagline || "";
  el.issuerEmail.value = issuer.email || "";
  el.issuerPhone.value = issuer.phone || "";
  el.issuerWebsite.value = issuer.website || "";
  el.issuerLocation.value = issuer.location || "";
}

function saveIssuerDefaults() {
  if (!el.issuerBrand) {
    return;
  }
  localStorage.setItem("budgetIssuerDefaults", JSON.stringify(issuerData()));
}

function initials(value) {
  return String(value || "")
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join("")
    .toUpperCase() || "PW";
}

function safeFileName(value) {
  return String(value || "presupuesto")
    .trim()
    .replace(/[^\w.-]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "") || "presupuesto";
}
