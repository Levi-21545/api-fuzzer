// Tela inicial: pacotes e campanhas encontrados em cada fonte.

import { getCatalog, getJson } from "../data.js";
import { badge, code, fmt, folderIcon, h, linkRow, na, notice, section } from "../dom.js";
import { href } from "../router.js";

// Grupos abertos nesta sessão; ao voltar ao catálogo eles continuam abertos.
const openGroups = new Set();

function parentOf(path) {
  const index = path.lastIndexOf("/");
  return index < 0 ? "" : path.slice(0, index);
}

export async function renderCatalog() {
  const catalog = await getCatalog();
  return h(
    "div",
    {},
    h("h1", {}, "Artefatos encontrados"),
    notice(
      "info",
      "Pacotes trazem os agregados publicados pela análise final. Campanhas avulsas são mostradas isoladamente: ",
      "seus números não entram em nenhum agregado desta interface.",
    ),
    catalog.sources.map((source) => renderSource(source)),
  );
}

function renderSource(source) {
  const groups = new Map();
  for (const campaign of source.campaigns) {
    const parent = parentOf(campaign);
    if (!groups.has(parent)) groups.set(parent, []);
    groups.get(parent).push(campaign);
  }
  return section(
    h("span", { class: "source-title", title: source.label }, folderIcon(), h("span", {}, source.path)),
    source.problems.map((problem) => notice("warn", problem)),
    source.packages.length === 0 && source.campaigns.length === 0
      ? h("p", { class: "muted" }, "Nenhum pacote ou campanha encontrado.")
      : null,
    source.packages.length
      ? h(
          "div",
          {},
          h("h3", {}, "Pacotes finais"),
          h("ul", { class: "plain" }, source.packages.map((dir) => packageItem(source.id, dir))),
        )
      : null,
    groups.size
      ? h(
          "div",
          {},
          h("h3", {}, "Campanhas avulsas"),
          [...groups].map(([parent, dirs]) => campaignGroup(source.id, parent, dirs)),
        )
      : null,
  );
}

function packageItem(sourceId, dir) {
  const summary = h("span", { class: "muted" }, " carregando…");
  getJson(sourceId, dir ? `${dir}/provenance-index.json` : "provenance-index.json").then((file) => {
    summary.textContent = "";
    if (file.state !== "ok") {
      summary.append(" — provenance-index.json ilegível");
      return;
    }
    const runs = Array.isArray(file.data.runs) ? file.data.runs.length : null;
    const commit = file.data.campaign_commit;
    summary.append(
      ` — ${runs == null ? "?" : fmt(runs)} campanhas listadas no provenance-index.json; fuzzer `,
      commit ? code(String(commit).slice(0, 12)) : na(),
    );
  });
  return h(
    "li",
    {},
    badge("pacote", "pkg"),
    " ",
    h("a", { href: href(["pkg", sourceId, dir]) }, dir || "(raiz da fonte)"),
    summary,
  );
}

function campaignGroup(sourceId, parent, dirs) {
  const key = `${sourceId}|${parent}`;
  const body = h("tbody", {});
  let loaded = false;

  // Os manifestos só são lidos quando o grupo é aberto.
  const load = () => {
    if (loaded) return;
    loaded = true;
    for (const dir of dirs) body.append(campaignRow(sourceId, parent, dir));
  };

  const group = h(
    "details",
    {
      class: "group",
      ontoggle: () => {
        if (group.open) {
          openGroups.add(key);
          load();
        } else {
          openGroups.delete(key);
        }
      },
    },
    h("summary", {}, badge("campanhas avulsas", "run"), parent || "(raiz da fonte)", h("span", { class: "muted" }, `${dirs.length} campanha${dirs.length === 1 ? "" : "s"}`)),
    h(
      "div",
      { class: "scroll" },
      h(
        "table",
        { class: "data" },
        h("thead", {}, h("tr", {}, ["Campanha", "Alvo (target_id)", "Experimento", "Status", "Início"].map((title) => h("th", {}, title)))),
        body,
      ),
    ),
  );
  if (openGroups.has(key)) {
    group.open = true;
    load();
  }
  return group;
}

function campaignRow(sourceId, parent, dir) {
  const target = href(["run", sourceId, dir]);
  const cells = {
    target: h("td", {}, "…"),
    experiment: h("td", {}, "…"),
    status: h("td", {}, "…"),
    started: h("td", {}, "…"),
  };
  getJson(sourceId, dir ? `${dir}/run_manifest.json` : "run_manifest.json").then((file) => {
    for (const cell of Object.values(cells)) cell.textContent = "";
    if (file.state !== "ok") {
      const reason = file.state === "missing" ? "sem run_manifest.json" : "run_manifest.json inválido";
      for (const cell of Object.values(cells)) cell.append(na(reason));
      return;
    }
    const manifest = file.data;
    cells.target.append(fmt(manifest.target_id));
    cells.experiment.append(fmt(manifest.experiment_id));
    cells.status.append(manifest.status ? badge(manifest.status, manifest.status === "completed" ? "ok" : "warn") : na());
    cells.started.append(fmt(manifest.started_at));
  });
  return linkRow(
    target,
    h("td", {}, h("a", { href: target }, dir.slice(parent ? parent.length + 1 : 0) || dir || "(raiz)")),
    cells.target,
    cells.experiment,
    cells.status,
    cells.started,
  );
}
