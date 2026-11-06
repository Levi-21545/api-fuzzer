// Construção de DOM sem innerHTML: todo texto vindo dos artefatos entra como
// textContent, então corpos de resposta nunca são interpretados como HTML.

import { countLabel } from "./labels.js";

export function h(tag, attrs = {}, ...children) {
  const element = document.createElement(tag);
  for (const [name, value] of Object.entries(attrs ?? {})) {
    if (value == null || value === false || name === "value") continue;
    if (name === "class") element.className = value;
    else if (name.startsWith("on")) element.addEventListener(name.slice(2), value);
    else element.setAttribute(name, value === true ? "" : value);
  }
  append(element, children);
  // Depois dos filhos, para que um <select> já tenha as opções.
  if (attrs?.value != null) element.value = attrs.value;
  return element;
}

function append(element, children) {
  for (const child of children) {
    if (child == null || child === false) continue;
    if (Array.isArray(child)) append(element, child);
    else if (child instanceof Node) element.appendChild(child);
    else element.appendChild(document.createTextNode(String(child)));
  }
}

const numberFormat = new Intl.NumberFormat("pt-BR");
const decimalFormat = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 4 });
// Uma casa, como em results.md; o valor exato está no JSON original.
const percentFormat = new Intl.NumberFormat("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

// Valor como texto; ausente vira "não disponível".
export function fmtText(value) {
  if (value === null || value === undefined) return "não disponível";
  if (typeof value === "number") {
    return Number.isInteger(value) ? numberFormat.format(value) : decimalFormat.format(value);
  }
  if (typeof value === "boolean") return value ? "sim" : "não";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

// Valor para célula: ausente vira um marcador visual "não disponível".
export function fmt(value) {
  return value === null || value === undefined ? na() : fmtText(value);
}

export function pct(value) {
  if (typeof value !== "number") return na();
  return `${percentFormat.format(value * 100)}%`;
}

export function na(reason) {
  return h("span", { class: "na", title: reason ?? null }, reason ? `não disponível (${reason})` : "não disponível");
}

export function code(text) {
  return h("code", {}, text);
}

export function shortId(id, length = 12) {
  if (typeof id !== "string") return na();
  return h("code", { title: id }, id.length > length ? `${id.slice(0, length)}…` : id);
}

export function badge(text, kind = "") {
  return h("span", { class: `badge ${kind}` }, text);
}

export function notice(kind, ...children) {
  return h("div", { class: `notice ${kind}` }, ...children);
}

export function section(title, ...children) {
  return h("section", { class: "card" }, h("h2", {}, title), ...children);
}

// Ícone de pasta em SVG (sem innerHTML); a cor vem de currentColor.
export function folderIcon() {
  const ns = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(ns, "svg");
  svg.setAttribute("viewBox", "0 0 16 16");
  svg.setAttribute("width", "16");
  svg.setAttribute("height", "16");
  svg.setAttribute("aria-hidden", "true");
  svg.setAttribute("class", "icon");
  const path = document.createElementNS(ns, "path");
  path.setAttribute("d", "M1.5 3.5A1 1 0 0 1 2.5 2.5h3.6l1.5 1.6h5.9a1 1 0 0 1 1 1v7.4a1 1 0 0 1-1 1H2.5a1 1 0 0 1-1-1z");
  path.setAttribute("fill", "none");
  path.setAttribute("stroke", "currentColor");
  path.setAttribute("stroke-width", "1.3");
  path.setAttribute("stroke-linejoin", "round");
  svg.appendChild(path);
  return svg;
}

// Faixa de prioridade do FIS com cor própria. A cor marca a faixa de triagem,
// não gravidade de segurança.
const BANDS = new Set(["LOW", "MEDIUM", "HIGH"]);
export function bandBadge(band) {
  if (band == null) return na();
  const known = BANDS.has(band);
  return h("span", { class: known ? `badge band band-${band.toLowerCase()}` : "badge", title: "Faixa de prioridade de triagem (FIS), não gravidade de segurança" }, band);
}

// Score mín–máx: um número só quando os dois são iguais.
export function scoreRange(range) {
  if (!Array.isArray(range) || range.length !== 2) return na();
  const [low, high] = range;
  return low === high ? fmtText(low) : `${fmtText(low)} – ${fmtText(high)}`;
}

// Tabela de pares chave/valor. `rows` é uma lista de [rótulo, valor].
// Layouts: padrão (rótulo em 45%), `end` (valores alinhados à direita, para
// cartões estreitos) e `wide` (rótulo de largura fixa, para cartões largos).
export function kvTable(rows, { layout = "" } = {}) {
  return h(
    "table",
    { class: layout ? `kv ${layout}` : "kv" },
    h(
      "tbody",
      {},
      rows.map(([label, value]) =>
        h("tr", {}, h("th", {}, label), h("td", {}, value instanceof Node ? value : fmt(value))),
      ),
    ),
  );
}

// Tabela de contagens de um objeto {chave: número}, com unidade explícita.
export function countTable(object, { unit, keyHeader = "Valor", labelKeys = false } = {}) {
  if (object == null) return na();
  const entries = Object.entries(object);
  if (entries.length === 0) return h("p", { class: "muted" }, "Nenhuma entrada.");
  return h(
    "table",
    { class: "data compact" },
    h("thead", {}, h("tr", {}, h("th", {}, keyHeader), h("th", { class: "num" }, unit ? unit[0].toUpperCase() + unit.slice(1) : "Quantidade"))),
    h(
      "tbody",
      {},
      entries.map(([key, value]) =>
        h("tr", {}, h("td", {}, labelKeys ? countLabel(key)[0] : code(key)), h("td", { class: "num" }, fmt(value))),
      ),
    ),
  );
}

// Bloco com o JSON original de um registro e o arquivo de onde ele veio.
export function rawJson(label, record, origin) {
  return h(
    "details",
    { class: "raw" },
    h("summary", {}, label, origin ? h("span", { class: "muted" }, ` — ${origin}`) : null),
    h("pre", {}, JSON.stringify(record, null, 2)),
  );
}

export function pre(text, kind = "") {
  return h("pre", { class: kind }, text);
}

// Linha de tabela inteira clicável que leva a `target`. O link da primeira
// célula continua existindo para teclado, leitores de tela e abrir em nova aba.
export function linkRow(target, ...cells) {
  return h(
    "tr",
    {
      class: "row-link",
      onclick: (event) => {
        if (event.target.closest("a, button, input, select, summary")) return;
        if (window.getSelection()?.toString()) return;
        location.hash = target;
      },
    },
    ...cells,
  );
}

// Faixa de contagens: [rótulo, valor, unidade]. O valor vem primeiro para que
// os números fiquem na mesma linha, qualquer que seja o tamanho do rótulo.
export function stats(items) {
  return h(
    "div",
    { class: "stats" },
    items.map(([label, value, unit]) =>
      h("div", { class: "stat" }, h("div", { class: "value" }, fmt(value)), h("div", { class: "label" }, label), unit ? h("div", { class: "unit" }, unit) : null),
    ),
  );
}

export function clear(element) {
  while (element.firstChild) element.removeChild(element.firstChild);
}
