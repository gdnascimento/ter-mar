/**
 * Fetch and cache the contract files. The only module that knows the on-disk
 * encoding: if the columnar fallback in docs/03-data-contracts.md is ever
 * adopted, rehydration happens here and nothing else changes.
 *
 * @module data
 */

/** @type {Map<string, Promise<unknown>>} */
const cache = new Map();

/** @param {string} path */
function load(path) {
  if (!cache.has(path)) {
    cache.set(
      path,
      fetch(`data/${path}`).then((r) => {
        if (!r.ok) throw new Error(`${path}: ${r.status}`);
        return r.json();
      }),
    );
  }
  return cache.get(path);
}

/** @returns {Promise<import('./types.js').Meta>} */
export function meta() {
  return /** @type {any} */ (load('meta.json'));
}

/** @returns {Promise<import('./types.js').Municipality[]>} */
export async function municipalities() {
  // TODO(M5): rehydrate here if the columnar encoding is adopted.
  throw new Error('not implemented');
}

/** @param {number} code */
export async function municipality(code) {
  throw new Error('not implemented');
}

/** @returns {Promise<Array<[number,string,string,string]>>} */
export async function searchIndex() {
  throw new Error('not implemented');
}

/**
 * @param {'residence'|'provider'} view
 * @returns {Promise<import('./types.js').FunnelCurves>}
 */
export async function funnelCurves(view) {
  throw new Error('not implemented');
}
