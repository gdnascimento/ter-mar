/**
 * Peer comparison table: região de saúde, then UF, then Brasil.
 *
 * Geographic adjacency is deliberately not used — a município across a state
 * line is in a different funding stream and referral network. The table carries
 * `labels.peersExplanation` because users will expect adjacency.
 *
 * Sorted by name. Never by SMR (invariant 6).
 *
 * @module peers
 */

/**
 * @param {import('./types.js').Municipality} selected
 * @param {import('./types.js').Municipality[]} all
 * @returns {import('./types.js').Municipality[]}
 */
export function peersOf(selected, all) {
  throw new Error('not implemented');
}

/**
 * @param {HTMLTableElement} table
 * @param {import('./types.js').Municipality[]} peers
 * @param {'residence'|'provider'} view
 */
export function render(table, peers, view) {
  throw new Error('not implemented');
}
