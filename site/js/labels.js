/**
 * Every user-visible string, in pt-BR. The only file in the project containing
 * Portuguese prose. Never inline a label in a component.
 *
 * Copy rules in docs/04-frontend.md: the verdicts are never "melhor" or "pior".
 */

export const labels = {
  searchPlaceholder: 'Busque seu município',
  tabResidence: 'Meus residentes',
  tabProvider: 'Hospitais daqui',

  smrName: 'Razão de mortalidade padronizada',
  smrShort: 'RMP',

  verdict: {
    within: 'compatível com a média nacional',
    above: 'acima do esperado',
    below: 'abaixo do esperado',
    insufficient: 'dados insuficientes para avaliar',
  },

  insufficientDetail:
    'O intervalo cobre desde muito abaixo até muito acima da média nacional, ' +
    'porque o número de casos é pequeno demais para distinguir.',

  staysPer100k: 'Internações em UTI por 100 mil habitantes',
  treatedOutside: 'Internações realizadas fora do município',
  bedsPer100k: 'Leitos de UTI por 100 mil habitantes',
  fromOthers: 'Pacientes vindos de outros municípios',
  noIcu: 'Este município não possui leitos de UTI',

  privateCoverage: 'Cobertura de planos de saúde',
  healthRegion: 'Região de saúde',
  population: 'População',

  methodologyLink: 'Como calculamos estes números',
  extractedAt: 'Dados do SIH/SUS extraídos em {date}',

  peersExplanation:
    'Comparamos com a região de saúde, e não com vizinhos no mapa, porque é a ' +
    'região que define para onde os pacientes são encaminhados.',

  peersHeading: 'Comparação com a região de saúde',
  stateHeading: 'Estado',
  nationalHeading: 'Brasil',
};
