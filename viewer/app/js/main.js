// Despacho das rotas e ciclo de renderização.

import { clearCache } from "./data.js";
import { clear, h, notice } from "./dom.js";
import { parseHash } from "./router.js";
import { renderCampaign, renderCase, renderSignature } from "./views/campaign.js";
import { renderCatalog } from "./views/catalog.js";
import { renderFile } from "./views/file.js";
import { renderPackage, renderPackageApi, renderSemanticId } from "./views/package.js";

const main = document.getElementById("main");
const scrollPositions = new Map();
let currentHash = null;
let renderToken = 0;

// Rota de campanha: dentro do pacote (kind "pkg") ou avulsa (kind "run"),
// seguida opcionalmente de sig/<id> ou case/<id>.
function campaignRoute(segments) {
  if (segments[0] === "run" && segments.length >= 3) {
    return { route: { kind: "run", source: segments[1], dir: segments[2] }, tail: segments.slice(3) };
  }
  if (segments[0] === "pkg" && segments[3] === "api" && segments[5] === "run" && segments.length >= 7) {
    return {
      route: { kind: "pkg", source: segments[1], pkgDir: segments[2], api: segments[4], runId: segments[6] },
      tail: segments.slice(7),
    };
  }
  return null;
}

function dispatch(segments, params) {
  if (segments.length === 0) return renderCatalog();
  const campaign = campaignRoute(segments);
  if (campaign) {
    const [kind, id] = campaign.tail;
    if (kind === undefined) return renderCampaign(campaign.route, params);
    if (kind === "sig" && id) return renderSignature(campaign.route, id, params);
    if (kind === "case" && id) return renderCase(campaign.route, id);
    return null;
  }
  if (segments[0] === "pkg" && segments.length >= 3) {
    const [, source, dir, sub, api, kind, id] = segments;
    if (sub === undefined) return renderPackage(source, dir);
    if (sub === "api" && api && kind === undefined) return renderPackageApi(source, dir, api, params);
    if (sub === "api" && api && kind === "id" && id) return renderSemanticId(source, dir, api, id);
  }
  if (segments[0] === "file" && segments.length === 3) return renderFile(segments[1], segments[2]);
  return null;
}

async function render(event) {
  // Os filtros mudam o hash com replaceState, sem evento; o endereço anterior
  // real vem de event.oldURL.
  const previous = event?.oldURL ? new URL(event.oldURL).hash : currentHash;
  if (previous !== null) scrollPositions.set(previous, window.scrollY);
  const samePage = previous !== null && previous.split("?")[0] === location.hash.split("?")[0];
  currentHash = location.hash;
  const token = ++renderToken;
  const { segments, params } = parseHash(location.hash);
  if (!samePage) {
    clear(main);
    main.append(h("p", { class: "muted" }, "Carregando…"));
  }
  let view;
  try {
    view = (await dispatch(segments, params)) ?? notice("error", "Endereço não reconhecido. ", h("a", { href: "#/" }, "Voltar ao início"));
  } catch (error) {
    view = notice("error", `Não foi possível ler os artefatos: ${error.message}`);
  }
  if (token !== renderToken) return;
  clear(main);
  main.append(view);
  window.scrollTo(0, scrollPositions.get(currentHash) ?? 0);
}

const themeSelect = document.getElementById("theme");
themeSelect.value = document.documentElement.dataset.theme ?? "auto";
themeSelect.addEventListener("change", () => {
  const choice = themeSelect.value;
  if (choice === "auto") delete document.documentElement.dataset.theme;
  else document.documentElement.dataset.theme = choice;
  try {
    if (choice === "auto") localStorage.removeItem("viewer-theme");
    else localStorage.setItem("viewer-theme", choice);
  } catch {
    // Sem armazenamento, o tema vale só até recarregar a página.
  }
});

document.getElementById("reload").addEventListener("click", () => {
  clearCache();
  currentHash = null;
  render();
});
window.addEventListener("hashchange", render);
render();
