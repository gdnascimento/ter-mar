# 04 — Frontend

Plain HTML and ES modules. **No build step, no bundler, no framework, no npm
install.** `site/` is served as-is. See
`docs/decisions/0005-no-build-step.md` for why.

Type safety across the JSON boundary comes from two places: the JSON Schemas in
`schemas/`, enforced in the pipeline, and JSDoc typedefs in `site/js/types.js`
that mirror them. If you change one, change the other in the same commit.

---

## Files

| Path | Responsibility |
| --- | --- |
| `site/index.html` | Search and result shell. The only page most visitors see |
| `site/metodologia.html` | Methodology. Partly rendered from `meta.json` so published figures cannot drift from the run |
| `site/css/main.css` | All styling. Custom properties, light and dark |
| `site/js/main.js` | Bootstrap, URL state (`?municipio=5208707`), view switching |
| `site/js/types.js` | JSDoc typedefs mirroring `schemas/`. No runtime code |
| `site/js/data.js` | Fetch, cache, rehydrate. The only module that knows the on-disk encoding |
| `site/js/labels.js` | **Every** user-visible string, in pt-BR. The only file containing Portuguese |
| `site/js/format.js` | pt-BR number, percentage and interval formatting |
| `site/js/search.js` | Accent-insensitive autocomplete over `busca.json` |
| `site/js/panel.js` | The two view panels and their stat tiles |
| `site/js/funnel.js` | Funnel plot, with the selected município highlighted |
| `site/js/peers.js` | Peer comparison table |
| `site/js/methodology.js` | Renders `metodologia.html` figures from `meta.json` |
| `site/vendor/` | Pinned third-party modules, committed. No CDN at runtime |

File and identifier names are English. The two HTML filenames are the
exception: they are URLs, and a Brazilian civic page gets Portuguese URLs.

---

## Page structure

```
index.html
├── header
│   ├── título + busca ("Busque seu município")
│   └── janela de dados + data de extração + link "Como calculamos"
├── resultado (hidden until a município is selected)
│   ├── cabeçalho: nome, UF, região de saúde, população
│   ├── abas: "Meus residentes" | "Hospitais daqui"
│   ├── três stat tiles
│   ├── gráfico de funil, com este município destacado
│   ├── tabela de pares (região de saúde, depois UF, depois Brasil)
│   └── faixa de contexto: cobertura de planos, leitos, população
└── footer: fonte, licença, repositório
```

The funnel plot is the centrepiece of each tab, not an appendix. It is what
stops the page being read as a ranking.

---

## Peers

The default peer set is the município's **região de saúde**, with UF and Brazil
as wider rings. Geographic adjacency is deliberately not used: a município
across a state line is in a different funding stream, referral network and CIR.

Users expect adjacency, so the page says in one line why they are not getting
it. The string is `labels.peersExplanation`.

---

## States that need real design

Three cases are the product, not edge cases.

**Suppressed.** Do not grey out and move on. Show the interval, show how wide
it is, and say so:

> dados insuficientes para avaliar — o intervalo cobre desde muito abaixo até
> muito acima da média nacional

**No ICU beds.** `provider.has_icu === false`:

> este município não possui leitos de UTI

Pair it with where residents are actually treated. For someone in a small
município this is the single most useful thing on the page.

**Data not yet loaded.** Skeleton, never a spinner over a half-rendered number.

---

## Copy rules

- Every ratio appears with its interval, at the same visual weight. There is no
  component that renders a bare point estimate (invariant 4).
- The three verdicts are *compatível com a média nacional*, *acima do esperado*,
  *abaixo do esperado*. **Never** *melhor* or *pior*.
- No ranking, no ordering by outcome, no top-N, no grade, no score
  (invariant 6).
- No downloadable file that is already sorted by SMR.
- The methodology link is in the header, not the footer.

---

## Label glossary

Starter contents of `labels.js`. Extend here, never inline.

| Key | pt-BR |
| --- | --- |
| `searchPlaceholder` | Busque seu município |
| `tabResidence` | Meus residentes |
| `tabProvider` | Hospitais daqui |
| `smrName` | Razão de mortalidade padronizada |
| `smrShort` | RMP |
| `verdict.within` | compatível com a média nacional |
| `verdict.above` | acima do esperado |
| `verdict.below` | abaixo do esperado |
| `verdict.insufficient` | dados insuficientes para avaliar |
| `staysPer100k` | Internações em UTI por 100 mil habitantes |
| `treatedOutside` | Internações realizadas fora do município |
| `bedsPer100k` | Leitos de UTI por 100 mil habitantes |
| `fromOthers` | Pacientes vindos de outros municípios |
| `noIcu` | Este município não possui leitos de UTI |
| `privateCoverage` | Cobertura de planos de saúde |
| `healthRegion` | Região de saúde |
| `methodologyLink` | Como calculamos estes números |
| `extractedAt` | Dados do SIH/SUS extraídos em {date} |
| `peersExplanation` | Comparamos com a região de saúde, e não com vizinhos no mapa, porque é a região que define para onde os pacientes são encaminhados. |

---

## Formatting

`format.js` wraps `Intl.NumberFormat('pt-BR')`. Decimal comma, thousands point.

- SMR: two decimals — `1,04`
- Interval: `1,04 (IC 95%: 0,99–1,09)`
- Percentage: one decimal plus `%`
- Counts: thousands separator
- Suppressed: an em dash, never `0`, `null` or `NaN`

---

## Accessibility and performance

- Every chart has a table alternative reachable without a mouse. The funnel plot
  carries `role="img"` and an `aria-label` stating the município's verdict in
  words.
- Keyboard-complete: search, tab switching, peer table.
- Contrast at WCAG AA in both themes. Verdict is never carried by colour alone —
  it always has a word.
- Budget: first view under 400 KB transferred, interactive under two seconds on
  3G. Much of this audience is on a phone, and the municípios that most need
  this page have the worst connectivity.
- Mobile layout first; the desktop layout is the enhancement.
