// Arquivo bruto de uma fonte, exibido como texto (Markdown e CSV não são
// renderizados, para que nenhum conteúdo seja interpretado como HTML).

import { fileUrl, getText } from "../data.js";
import { code, fmtText, h, notice, pre } from "../dom.js";

const PREVIEW_CHARS = 500_000;

export async function renderFile(source, path) {
  const text = await getText(source, path);
  const head = [
    h("p", { class: "crumbs" }, h("a", { href: "#/" }, "Artefatos"), " / arquivo"),
    h("h1", {}, code(path)),
  ];
  if (text === null) return h("div", {}, head, notice("error", "Arquivo inexistente nesta fonte."));
  const block = pre(text.length > PREVIEW_CHARS ? text.slice(0, PREVIEW_CHARS) : text, "body file");
  const more =
    text.length > PREVIEW_CHARS
      ? h(
          "button",
          {
            type: "button",
            onclick: (event) => {
              block.textContent = text;
              event.target.remove();
            },
          },
          `mostrar completo (${fmtText(text.length)} caracteres)`,
        )
      : null;
  return h(
    "div",
    {},
    head,
    h("p", { class: "muted" }, `${fmtText(text.length)} caracteres, exibidos como texto. `, h("a", { href: fileUrl(source, path), target: "_blank", rel: "noopener" }, "abrir o arquivo cru")),
    block,
    more,
  );
}
