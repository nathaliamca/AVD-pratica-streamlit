# Justificativa das métricas — Dashboard 2

O Dashboard 2 mostra um resumo das pessoas da base de obesidade. As quatro métricas ajudam a entender o grupo que aparece depois de aplicar os filtros.

## Quantidade de participantes

Mostra quantas pessoas estão no grupo selecionado. Esse número é importante porque os filtros podem deixar o grupo bem pequeno. Assim, dá para saber quantos registros estão sendo usados nos outros cálculos. É uma contagem simples.

## Percentual classificado como Obeso

Mostra qual parte do grupo está classificada como Obeso. O percentual ajuda a comparar grupos com quantidades diferentes de pessoas, em vez de olhar só o número de casos. O cálculo divide a quantidade de pessoas nessa classificação pelo total do grupo e multiplica por 100.

## Idade média

Ajuda a entender a idade das pessoas do grupo e como esse perfil muda com os filtros. É calculada somando as idades e dividindo pela quantidade de idades válidas. A média sozinha não mostra se as pessoas têm idades próximas ou muito diferentes.

## Peso médio

Resume o peso do grupo em quilos e permite observar como ele muda ao selecionar pessoas com características diferentes. O cálculo soma os pesos e divide pela quantidade de pesos válidos. Pessoas com pesos muito altos ou baixos podem influenciar a média, por isso ela aparece junto dos gráficos. O peso sozinho não determina a classificação de obesidade.

O histograma de peso complementa essa média, mostrando quantas pessoas estão em cada faixa de peso. Assim, dá para observar se os pesos estão mais próximos ou espalhados, algo que a média sozinha não mostra.

## Como os filtros entram nos cálculos

Os filtros de gênero, idade e histórico familiar atualizam as quatro métricas. Ao selecionar uma região no gráfico de idade e peso, os números, o gráfico de barras e o histograma de peso passam a considerar somente as pessoas daquela região. Sem essa seleção, são usadas todas as pessoas que atendem aos filtros.

Não foi colocado um filtro para mostrar apenas Obeso, porque isso faria o percentual ficar sempre em 100%. Também não há filtro por período, pois a base não tem datas.

## O que considerar na leitura

Os resultados se referem a esta base, que também contém registros gerados artificialmente, e não representam toda a população. A classificação Não Obeso inclui outras categorias além de peso normal, conforme o agrupamento feito na análise original.

Quando os filtros não retornam ninguém, a quantidade fica em zero e as outras métricas mostram “—”. Esse símbolo também aparece quando não há valores válidos para calcular uma média. Os gráficos ajudam a observar diferenças que as médias não mostram, mas as relações vistas neles não provam que uma variável causa a outra.
