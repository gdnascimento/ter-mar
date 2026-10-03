/**
 * Bootstrap: URL state, search wiring, panel rendering, tab switching.
 *
 * URL contract: `?municipio=5208707`. A result must be a shareable link — for a
 * civic tool that is not a nicety, it is how the page spreads.
 *
 * @module main
 */

import { labels } from './labels.js';
import * as data from './data.js';

/** Fill every `data-label` placeholder in the static shell from labels.js. */
function applyLabels() {
  throw new Error('not implemented');
}

/** Fill every `data-meta` placeholder from meta.json. */
async function applyMeta() {
  throw new Error('not implemented');
}

/** @returns {number|null} the municipality code in the URL, if any */
function codeFromUrl() {
  const value = new URLSearchParams(location.search).get('municipio');
  return value && /^\d{7}$/.test(value) ? Number(value) : null;
}

/** @param {number} code */
function selectMunicipality(code) {
  throw new Error('not implemented');
}

async function boot() {
  throw new Error('not implemented');
}

boot();
