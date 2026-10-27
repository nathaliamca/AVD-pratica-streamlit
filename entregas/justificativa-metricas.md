# Justificativa das métricas — Dashboard 2

O dashboard “Perfil da amostra” apresenta o grupo selecionado na base de obesidade. Seu público são pessoas interessadas em explorar o perfil dos participantes e comparar recortes da amostra.

| Métrica | Relação com métricas básicas | Por que foi escolhida e o que comunica |
| --- | --- | --- |
| Participantes | Contagem absoluta de linhas | Mostra o tamanho do grupo. Dá contexto às médias e proporções, especialmente quando os filtros deixam poucos registros. |
| Obeso no recorte (%) | Proporção: 100 × registros classificados como Obeso / total do recorte | Permite comparar a composição de grupos com tamanhos diferentes. O denominador é sempre a contagem de participantes exibida ao lado. |
| Idade média (anos) | Média aritmética dos valores válidos de Age | Resume o perfil etário do grupo. Ajuda a contextualizar comparações entre filtros, sem substituir a distribuição de idades. |
| Peso médio (kg) | Média aritmética dos valores válidos de Weight | Resume o peso dos participantes selecionados. Deve ser lida junto da dispersão e das categorias de peso; peso isolado não define diagnóstico. |

## Filtros e seleção vinculada

Gênero, idade e histórico familiar definem o recorte inicial, independentemente do Dashboard 1. Arrastar uma região no gráfico idade × peso restringe esse recorte e atualiza as quatro métricas e as barras de categorias. Sem seleção gráfica, usar todos os participantes que atendem aos filtros. O app informa as duas contagens.

As barras mostram contagens por categoria original, em ordem fixa, incluindo categorias com zero participantes. A dispersão mostra heterogeneidade que as médias escondem. Ambos usam Altair.

Não há filtro de status de obesidade: selecionar apenas Obeso tornaria a proporção trivialmente 100%. Não há filtro de período nem deltas, pois a base não tem datas ou meta de comparação definida.

## Cuidados de interpretação e casos vazios

- Sem participantes: contagem 0 e demais métricas “—”; não calcular divisão por zero.
- Sem valores válidos para uma média: mostrar “—”.
- Não Obeso segue o agrupamento da EDA e inclui categorias além de peso normal.
- A base contém registros sintéticos. O percentual descreve os registros deste recorte e não representa uma estimativa de prevalência populacional.
- Médias são sensíveis a valores extremos. Os gráficos complementam a leitura dos cartões.
- Associações observadas são descritivas, sem estabelecer causa e efeito.

Planejamento anterior à implementação: `planejamento-dashboard2.md`. Layout: `rascunho-dashboard2.png`.
