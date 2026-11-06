// Acesso ao servidor local e cache em memória da sessão. Nada é gravado no
// navegador nem em disco.

import { loadCampaign, loadPackage } from "./model.js";

const cache = new Map();

export function clearCache() {
  cache.clear();
}

function remember(key, load) {
  if (!cache.has(key)) {
    const promise = load();
    cache.set(key, promise);
    promise.catch(() => cache.delete(key));
  }
  return cache.get(key);
}

async function errorMessage(response) {
  try {
    const body = await response.json();
    return body.error ?? response.statusText;
  } catch {
    return response.statusText;
  }
}

export function fileUrl(source, path) {
  return `/api/file?source=${encodeURIComponent(source)}&path=${encodeURIComponent(path)}`;
}

// Leitor de arquivos de uma fonte: devolve o texto, ou null se não existir.
export function readerFor(source) {
  return {
    async text(path) {
      const response = await fetch(fileUrl(source, path));
      if (response.status === 404) return null;
      if (!response.ok) throw new Error(`${path}: ${await errorMessage(response)}`);
      return response.text();
    },
  };
}

export function getCatalog() {
  return remember("catalog", async () => {
    const response = await fetch("/api/catalog");
    if (!response.ok) throw new Error(`catálogo: ${await errorMessage(response)}`);
    return response.json();
  });
}

export function getPackage(source, dir) {
  return remember(`pkg|${source}|${dir}`, () => loadPackage(readerFor(source), dir));
}

export function getCampaign(source, dir) {
  return remember(`run|${source}|${dir}`, () => loadCampaign(readerFor(source), dir));
}

export function getText(source, path) {
  return remember(`text|${source}|${path}`, () => readerFor(source).text(path));
}

export function getJson(source, path) {
  return remember(`json|${source}|${path}`, async () => {
    const text = await readerFor(source).text(path);
    if (text === null) return { state: "missing" };
    try {
      return { state: "ok", data: JSON.parse(text) };
    } catch (error) {
      return { state: "invalid", message: error.message };
    }
  });
}
