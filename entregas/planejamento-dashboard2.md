# Planejamento do Dashboard 2 — Perfil da amostra

Etapa 4 da Aula 22. Definições feitas antes do rascunho e da implementação do Dashboard 2.

## 1. Variáveis selecionadas

- `Age`: idade em anos, para filtro, média e dispersão.
- `Weight`: peso em kg, para média e dispersão.
- `Gender`: gênero registrado na base, para filtro.
- `family_history_with_overweight`: histórico familiar de sobrepeso, para filtro.
- `status_obesidade`: classificação binária criada na EDA, para proporção e cores.
- `NObeyesdad`: sete categorias originais de peso, para gráfico de contagens.

Fonte: `data/clean/dataset.csv`, com o tratamento da EDA preservado.
Público: pessoas que desejam explorar o perfil dos participantes desta base.

## 2. Métricas propostas

Todas usam o mesmo recorte após os filtros e, quando existir, a seleção no gráfico.

| Métrica | Cálculo | Tipo de métrica básica | O que comunica |
| --- | --- | --- | --- |
| Participantes | Número de linhas | Contagem absoluta | Tamanho do grupo e contexto das demais métricas. |
| Classificados como Obeso (%) | 100 × quantidade com status Obeso / participantes | Proporção relativa | Participação dessa classificação dentro do grupo selecionado. |
| Idade média (anos) | Soma de Age / valores válidos de Age | Média aritmética | Idade central do recorte. |
| Peso médio (kg) | Soma de Weight / valores válidos de Weight | Média aritmética | Resumo do peso do grupo, sem interpretar peso isolado como diagnóstico. |

Sem participantes: contagem zero, demais métricas como “—” e aviso para ampliar os filtros. Não dividir por zero.
Sem valores válidos em uma medida: mostrar “—” para sua média.
Não usar deltas: não há período temporal ou meta definidos para comparação.
“Não Obeso” reúne as categorias restantes conforme a EDA; não significa necessariamente peso normal.
A proporção descreve esta base, que inclui registros sintéticos, e não estima a prevalência na população.

## 3. Widgets definidos antes do rascunho

| Widget | Opções e padrão | Efeito |
| --- | --- | --- |
| Seletor de gênero | Todos (padrão), Feminino, Masculino; mapear para Gender | Filtrar o Dashboard 2. |
| Slider de idade | Limites da base; intervalo completo por padrão | Filtrar Age com limites inclusivos. |
| Seletor de histórico familiar | Todos (padrão), Sim, Não; mapear para yes/no | Filtrar family_history_with_overweight. |
| Botão “Limpar filtros” | Restaurar padrões e remover seleção gráfica | Voltar ao recorte completo. |

Não filtrar por status de obesidade inicialmente: selecionar apenas Obeso tornaria a proporção automaticamente 100%.
Os filtros serão independentes dos sliders do Dashboard 1, com chaves próprias.
Como a base não contém datas, não usar seletor de período.

## 4. Layout e interação planejados

Rascunho: `entregas/rascunho-dashboard2.png`.

- Abas principais futuras: Dashboard 1 e Dashboard 2.
- Título “Perfil da amostra”, seguido de uma faixa horizontal de filtros.
- Quatro cartões de métricas e dois gráficos Altair.
- Barras: participantes em cada categoria original de peso, com rótulos em português e ordem fixa das sete categorias.
- Dispersão: idade × peso, com cor por status e tooltip com idade, peso e categoria.
- Seleção de uma região na dispersão: métricas e barras usam os participantes selecionados. Sem seleção, usar todo o recorte dos widgets.
- Na implementação, usar a seleção retornada pelo Streamlit para aplicar o mesmo recorte às métricas e às barras; uma seleção Altair isolada não atualiza automaticamente st.metric.
- Exibir contagens antes e depois da seleção gráfica para deixar explícito o denominador das métricas.

## Identidade visual

Paleta inspirada em Summer Sunset: fundo creme `#FFF8F2`, superfícies pêssego `#FFEEE5`, destaque coral escuro `#C74736`, coral `#ED6A5A`, dourado `#F6B65B` e roxo `#6A3D78`. Texto escuro `#39263F` e fonte sans serif.
Roxo representa Obeso e coral representa Não Obeso, com a mesma convenção no app.
O dourado é apoio visual, sem texto claro sobre ele.
O rascunho é esquemático, sem métricas calculadas ou resultados simulados.
