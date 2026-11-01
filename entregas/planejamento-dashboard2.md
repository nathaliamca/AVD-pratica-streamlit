# Planejamento do Dashboard 2 — Perfil da amostra

A ideia deste dashboard é mostrar um resumo das pessoas da base de obesidade e permitir comparar grupos usando os filtros. Os dados usados são os mesmos que foram tratados na análise original.

## 1. Informações usadas

- Idade: para selecionar uma faixa etária, calcular a média e comparar com o peso.
- Peso: para calcular a média e mostrar sua relação com a idade.
- Gênero: para filtrar o grupo.
- Histórico familiar de sobrepeso: para comparar pessoas com e sem esse histórico.
- Classificação Obeso ou Não Obeso: para calcular o percentual e separar as cores dos pontos.
- As sete categorias originais de peso: para mostrar a quantidade de pessoas em cada uma.

## 2. Números que aparecem no painel

O painel terá quatro cartões:

- Quantidade de participantes: quantas pessoas ficaram no grupo depois dos filtros.
- Percentual classificado como Obeso: qual parte desse grupo tem essa classificação.
- Idade média: um resumo das idades das pessoas selecionadas.
- Peso médio: um resumo dos pesos, em quilos.

A quantidade é uma contagem, o percentual é uma proporção e os outros dois valores são médias. Todos devem considerar o mesmo grupo. Os motivos de cada escolha estão no arquivo de justificativa das métricas.

Se os filtros não retornarem ninguém, a quantidade será zero e os outros cartões mostrarão “—”. Não haverá comparação com meses anteriores, porque a base não tem datas.

## 3. Filtros

Antes de desenhar a tela, os controles definidos foram:

- Gênero: Todos, Feminino ou Masculino.
- Intervalo de idade: uma barra para escolher a menor e a maior idade do grupo, incluindo os dois limites.
- Histórico familiar de sobrepeso: Todos, Sim ou Não.
- Limpar filtros: um botão para voltar às opções iniciais e desfazer a seleção feita no gráfico.

Ao abrir o dashboard, todas as pessoas da base estarão incluídas. Esses filtros serão separados dos usados no Dashboard 1.

Não haverá um filtro para selecionar apenas Obeso, pois isso faria o percentual ficar sempre em 100%.

## 4. Organização da tela

O aplicativo terá duas abas principais: Dashboard 1 e Dashboard 2. Na segunda, o título será “Perfil da amostra”. Os filtros ficarão em uma faixa no topo, seguidos pelos quatro cartões.

Abaixo dos cartões, haverá dois gráficos feitos com Altair:

- Barras: mostram quantas pessoas estão em cada uma das sete categorias de peso, com os nomes em português. As categorias sem participantes também aparecerão, com quantidade zero.
- Idade e peso: cada ponto representa um registro da base. As cores separam Obeso e Não Obeso. Ao passar o mouse, aparecem a idade, o peso e a categoria.

Ao arrastar e selecionar uma região no gráfico de idade e peso, os cartões e as barras serão atualizados para esse grupo. Sem essa seleção, serão consideradas todas as pessoas que atendem aos filtros. A tela também mostrará quantas pessoas ficaram após os filtros e quantas entraram no cálculo dos cartões.

O desenho dessa organização está em [rascunho-dashboard2.png](rascunho-dashboard2.png).

## 5. Cores

A paleta escolhida é Summer Sunset, com fundo creme, áreas em pêssego e detalhes em coral, dourado e roxo. O texto será escuro para facilitar a leitura.

Nos gráficos, roxo representa Obeso e coral representa Não Obeso. Essa combinação será mantida nos dois dashboards.

## Cuidados com os resultados

A classificação Não Obeso segue o agrupamento da análise original e inclui outras categorias além de peso normal. O peso médio deve ser observado junto dos gráficos, pois sozinho não determina a classificação de obesidade.

Os números descrevem esta base, que também contém registros gerados artificialmente. Eles não representam toda a população.
