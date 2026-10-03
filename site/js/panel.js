/**
 * The two view panels and their stat tiles.
 *
 * Rules this module must not break:
 *  - a tile showing an SMR always shows its interval, at the same visual weight
 *  - a suppressed value renders the insufficient copy, never a greyed-out box
 *  - `provider.has_icu === false` renders `labels.noIcu` plus where residents
 *    are actually treated, which is the most useful thing on the page for a
 *    small município
 *
 * @module panel
 */

/**
 * @param {HTMLElement} root
 * @param {import('./types.js').Municipality} municipality
 * @param {'residence'|'provider'} view
 */
export function render(root, municipality, view) {
  throw new Error('not implemented');
}
