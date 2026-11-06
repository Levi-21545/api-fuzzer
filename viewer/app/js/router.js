// Rotas no hash da URL: #/seg/seg?filtro=valor. Cada segmento é codificado
// por inteiro, então caminhos com "/" ocupam um único segmento. Os filtros
// ficam na query para que Voltar e links copiados preservem o estado.

export function parseHash(hash) {
  const body = hash.replace(/^#\/?/, "");
  const [path, query = ""] = body.split("?");
  const segments = path ? path.split("/").map(decodeURIComponent) : [];
  const params = {};
  for (const [key, value] of new URLSearchParams(query)) params[key] = value;
  return { segments, params };
}

export function href(segments, params = {}) {
  const path = segments.map((segment) => encodeURIComponent(String(segment))).join("/");
  const query = new URLSearchParams(
    Object.entries(params).filter(([, value]) => value != null && value !== ""),
  ).toString();
  return `#/${path}${query ? `?${query}` : ""}`;
}

// Atualiza a query sem criar entrada no histórico (usado pelos filtros).
export function replaceParams(segments, params) {
  history.replaceState(null, "", href(segments, params));
}
