# Prompt de layout — síntese da conversa

Coloque os filtros na lateral e os gráficos de distribuição e correlação em abas, com nomes em português. Pode fazer um rascunho bem simples mostrando essa organização?

## Contexto

Estou fazendo os dashboards das Aulas 21 e 22 com meu dataset de obesidade. Como organizo o app usando minha EDA original e o CSV tratado em `data/clean/`?

## Entrada

Coloque os filtros na lateral e os gráficos de distribuição e correlação em abas, com nomes em português. Pode fazer um rascunho bem simples mostrando essa organização?

Para o Dashboard 2, quais métricas e filtros fazem sentido? Defina primeiro as variáveis, as métricas e os widgets, e só depois faça o rascunho.

Imagens registradas: `entregas/rascunho-dashboard1.png` e `entregas/rascunho-dashboard2.png`.

## Restrições

Mantenha minha análise original e carregue o dado tratado por `src/data_loader.py`. Use Plotly no Dashboard 1, Altair no Dashboard 2 e a paleta Summer Sunset. Como trato os casos em que nenhuma variável está selecionada ou os filtros não retornam participantes?

## Formato de saída

Coloque duas abas principais no `app.py`: Dashboard 1 e Dashboard 2. No segundo, use os filtros do rascunho, métricas com `st.metric` e gráficos Altair. Explique como os filtros e a seleção no gráfico atualizam os valores e teste se os recálculos estão certos.
