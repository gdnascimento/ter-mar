/**
 * Accent-insensitive autocomplete over busca.json.
 *
 * The `normalized` column is precomputed in the pipeline, so this module never
 * normalises 5,570 strings at load.
 *
 * Keyboard-complete by contract (docs/04-frontend.md): arrow keys move the
 * active option, Enter selects, Escape closes, and `aria-activedescendant`
 * tracks the active option.
 *
 * @module search
 */

/**
 * @param {string} query
 * @param {Array<[number,string,string,string]>} index
 * @param {number} limit
 * @returns {Array<[number,string,string,string]>}
 */
export function match(query, index, limit = 8) {
  throw new Error('not implemented');
}

/**
 * @param {HTMLInputElement} input
 * @param {HTMLElement} listbox
 * @param {(code: number) => void} onSelect
 */
export function attach(input, listbox, onSelect) {
  throw new Error('not implemented');
}
