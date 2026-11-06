// Tabela com filtros, busca e paginação. O estado dos filtros vive na query
// do hash; mudar um filtro substitui a entrada atual do histórico, então
// Voltar a partir de um detalhe reabre a tabela com os mesmos filtros.
// Colunas com `sort` (função linha → valor) e `key` podem ser ordenadas pelo
// cabeçalho: crescente, decrescente e de volta à ordem padrão. `defaultSort`
// ({key, dir, label}) define a ordem inicial; sem ele, vale a ordem do arquivo.

import { clear, fmt, h } from "./dom.js";
import { distinctValues, filterRows, paginate, sortRows } from "./model.js";
import { replaceParams } from "./router.js";

const PAGE_SIZE = 100;

export function filterableTable({
  segments,
  params,
  rows,
  filters = [],
  toggles = [],
  searchFields = [],
  searchPlaceholder = "buscar",
  columns,
  unit,
  prefilter,
  defaultSort = null,
}) {
  const state = { ...params };
  const spec = Object.fromEntries(filters.map((filter) => [filter.name, filter.field]));
  const body = h("div", { class: "table-body" });

  const update = (name, value) => {
    state[name] = value;
    if (name !== "p") delete state.p;
    replaceParams(segments, state);
    render();
  };

  const active = () => filters.some((filter) => state[filter.name]) || toggles.some((toggle) => state[toggle.name] === "1") || Boolean(state.q) || Boolean(state.ordem);

  const clearButton = h("button", { type: "button", class: "link-button", onclick: () => reset() }, "Limpar filtros");

  // Busca em linha própria; seletores em grade, com o rótulo acima.
  const controls = h(
    "div",
    { class: "filters" },
    h(
      "div",
      { class: "filters-search" },
      h("input", {
        type: "search",
        placeholder: searchPlaceholder,
        value: state.q ?? "",
        "aria-label": "Buscar",
        oninput: (event) => update("q", event.target.value),
      }),
      clearButton,
    ),
    filters.length
      ? h(
          "div",
          { class: "filters-grid" },
          filters.map((filter) => {
            const options = filter.options ?? distinctValues(rows, filter.field);
            return h(
              "label",
              { class: "field" },
              h("span", {}, filter.label),
              h(
                "select",
                { value: state[filter.name] ?? "", onchange: (event) => update(filter.name, event.target.value) },
                h("option", { value: "" }, "todas"),
                options.map((option) => h("option", { value: option }, option)),
              ),
            );
          }),
        )
      : null,
    toggles.length
      ? h(
          "div",
          { class: "filters-toggles" },
          toggles.map((toggle) =>
            h(
              "label",
              { class: "toggle" },
              h("input", {
                type: "checkbox",
                checked: state[toggle.name] === "1",
                onchange: (event) => update(toggle.name, event.target.checked ? "1" : ""),
              }),
              ` ${toggle.label}`,
            ),
          ),
        )
      : null,
  );

  function reset() {
    for (const filter of filters) delete state[filter.name];
    for (const toggle of toggles) delete state[toggle.name];
    delete state.q;
    delete state.p;
    delete state.ordem;
    delete state.dir;
    replaceParams(segments, state);
    const fresh = filterableTable({ segments, params: state, rows, filters, toggles, searchFields, searchPlaceholder, columns, unit, prefilter, defaultSort });
    wrapper.replaceWith(fresh);
  }

  function render() {
    clear(body);
    clearButton.disabled = !active();
    for (const select of controls.querySelectorAll("select")) select.classList.toggle("set", select.value !== "");
    const base = prefilter ? prefilter(rows, state) : rows;
    const filtered = filterRows(base, state, spec, searchFields);
    const explicit = columns.find((column) => column.sort && column.key === state.ordem);
    const sortColumn = explicit ?? (defaultSort ? columns.find((column) => column.sort && column.key === defaultSort.key) : null);
    const direction = explicit ? (state.dir === "desc" ? "desc" : "asc") : defaultSort?.dir === "desc" ? "desc" : "asc";
    const matched = sortColumn ? sortRows(filtered, sortColumn.sort, direction) : filtered;
    const page = paginate(matched, Number(state.p), PAGE_SIZE);
    body.append(
      h(
        "p",
        { class: "count" },
        `${fmt(matched.length)} de ${fmt(rows.length)} ${unit}`,
        base.length !== rows.length ? ` (${fmt(rows.length - base.length)} ocultas pela opção acima)` : "",
      ),
      h(
        "div",
        { class: "scroll" },
        h(
          "table",
          { class: "data" },
          h("thead", {}, h("tr", {}, columns.map((column) => header(column, sortColumn === column ? direction : null)))),
          h(
            "tbody",
            {},
            page.rows.map((row) => h("tr", {}, columns.map((column) => h("td", { class: column.class ?? "" }, column.cell(row))))),
          ),
        ),
      ),
      page.pages > 1 ? pager(page, (next) => update("p", String(next))) : "",
    );
  }

  // Ciclo do clique: crescente → decrescente → ordem padrão. Na coluna da
  // ordem padrão, o clique só alterna entre as duas direções.
  function header(column, current) {
    const attrs = { class: column.class ?? "", title: column.title ?? null };
    if (!column.sort) return h("th", attrs, column.header);
    let next = current === null ? "asc" : current === "asc" ? "desc" : null;
    if (next === null && defaultSort?.key === column.key && (defaultSort.dir ?? "asc") === current) next = current === "asc" ? "desc" : "asc";
    const label = { asc: "crescente", desc: "decrescente" };
    const resetTitle = defaultSort ? `Voltar à ordem padrão (${defaultSort.label})` : "Voltar à ordem do arquivo";
    return h(
      "th",
      { ...attrs, class: `${attrs.class} sortable`, "aria-sort": current ? (current === "asc" ? "ascending" : "descending") : "none" },
      h(
        "button",
        {
          type: "button",
          class: current ? "sort active" : "sort",
          title: next ? `Ordenar em ordem ${label[next]}` : resetTitle,
          onclick: () => {
            state.ordem = next ? column.key : "";
            state.dir = next === "desc" ? "desc" : "";
            delete state.p;
            replaceParams(segments, state);
            render();
          },
        },
        column.header,
        h("span", { class: "arrow", "aria-hidden": "true" }, current === "asc" ? "▲" : current === "desc" ? "▼" : "↕"),
      ),
    );
  }

  const wrapper = h("div", { class: "filterable" }, controls, body);
  render();
  return wrapper;
}

function pager(page, go) {
  return h(
    "nav",
    { class: "pager" },
    h("button", { type: "button", disabled: page.page <= 1, onclick: () => go(page.page - 1) }, "← anterior"),
    ` página ${page.page} de ${page.pages} `,
    h("button", { type: "button", disabled: page.page >= page.pages, onclick: () => go(page.page + 1) }, "próxima →"),
  );
}
