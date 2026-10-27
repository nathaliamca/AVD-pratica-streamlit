import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_data
from src.dashboard1 import calcular_correlacao
from src.dashboard2 import (filtrar_perfil, aplicar_selecao, calcular_metricas,
    criar_dispersao, criar_barras)

st.set_page_config(
    page_title="Análise de obesidade",
    layout="wide",
)

# Oculta as barras de ferramentas, preservando o botão da sidebar.
st.html("""
<style>
[data-testid="stElementToolbar"] { display: none !important; }
[data-testid="stToolbar"],
[data-testid="stAppToolbar"] { display: none !important; }
</style>
""")

st.caption("EXPLORAÇÃO DE DADOS · HÁBITOS E CONDIÇÃO FÍSICA")
st.title("Obesidade: explorando os dados")
st.write("Explore a distribuição das medidas e as relações entre as variáveis da base.")

df = load_data()

# Variáveis quantitativas do estudo (mesma lista VARS_QUANT do notebook de EDA)
VARS_QUANT = ["Age", "Height", "Weight", "FCVC", "NCP", "CH2O", "FAF", "TUE"]
NOMES = {
    "Age": "Idade (anos)", "Height": "Altura (m)", "Weight": "Peso (kg)",
    "FCVC": "Consumo de vegetais", "NCP": "Refeições principais",
    "CH2O": "Consumo de água", "FAF": "Atividade física",
    "TUE": "Uso de dispositivos eletrônicos",
}

dashboard1, dashboard2 = st.tabs(["Dashboard 1", "Dashboard 2"])

with dashboard1:
    # Sidebar: filtros (variáveis + intervalo)
    with st.sidebar:
        st.header("Filtros do Dashboard 1")
        st.caption("Escolha as medidas e ajuste os intervalos da análise.")

        variaveis = st.multiselect(
            "Variáveis da análise",
            options=VARS_QUANT,
            default=VARS_QUANT,
            format_func=lambda nome: NOMES.get(nome, nome),
            help="Selecione as variáveis quantitativas que deseja analisar no dashboard.",
        )

        separar_por_classe = st.toggle(
            "Comparar por status de obesidade",
            value=False,
            help="Separa o histograma em Obeso e Não Obeso, conforme sua EDA.",
        )

        # Um slider de intervalo para cada variável selecionada
        intervalos = {}
        for var in variaveis:
            if pd.api.types.is_integer_dtype(df[var]):
                minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
            else:
                minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.01
            if minimo == maximo:
                st.caption(f"{NOMES[var]}: valor único ({minimo:g}); sem intervalo para ajustar.")
                intervalos[var] = (minimo, maximo)
                continue
            intervalos[var] = st.slider(
                f"Intervalo: {NOMES[var]}",
                min_value=minimo,
                max_value=maximo,
                value=(minimo, maximo),
                step=passo,
                key=f"intervalo_{var}",
            )

    # Mantém só os pacientes dentro de todos os intervalos escolhidos
    df_filtrado = df
    for var, (inicio, fim) in intervalos.items():
        df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

    st.caption(f"{len(df_filtrado)} de {len(df)} participantes dentro dos intervalos escolhidos.")

    if not variaveis:
        st.info("Selecione uma ou mais variáveis na lateral para começar.")
    elif df_filtrado.empty:
        st.info("Nenhum participante neste recorte. Amplie os intervalos na lateral.")
    else:
        tab_distribuicao, tab_correlacao = st.tabs(["Distribuição", "Relações entre variáveis"])
        with tab_distribuicao:
            st.subheader("Como os valores se distribuem?")
            var_hist = st.selectbox(
                "Medida para explorar", variaveis,
                format_func=lambda nome: NOMES.get(nome, nome),
                key="variavel_histograma",
            )
            fig = px.histogram(
                df_filtrado, x=var_hist,
                color="status_obesidade" if separar_por_classe else None,
                labels={**NOMES, "status_obesidade": "Status de obesidade"},
                color_discrete_sequence=["#C74736"],
                color_discrete_map={"Obeso": "#6A3D78", "Não Obeso": "#ED6A5A"},
                barmode="overlay", opacity=0.75, nbins=20,
            )
            fig.update_layout(yaxis_title="Participantes", bargap=0.04, height=430, dragmode=False)
            st.plotly_chart(fig, width="stretch", key="histograma",
                config={"displayModeBar": False, "scrollZoom": False})

        with tab_correlacao:
            st.subheader("Quais medidas variam juntas?")
            st.caption("Correlação de Spearman: valores próximos de −1 ou 1 indicam associações mais fortes.")
            if len(variaveis) < 2 or len(df_filtrado) < 2:
                st.info("Selecione ao menos duas variáveis e mantenha dois ou mais participantes.")
            else:
                matriz = calcular_correlacao(df_filtrado[variaveis])
                matriz = matriz.rename(index=NOMES, columns=NOMES)
                fig_corr = px.imshow(
                    matriz, text_auto=".2f", zmin=-1, zmax=1,
                    color_continuous_scale=["#6A3D78", "#FFF8F2", "#C74736"],
                    aspect="auto", labels={"color": "Spearman"},
                )
                fig_corr.update_layout(height=550, dragmode=False)
                st.plotly_chart(fig_corr, width="stretch", key="correlacao",
                    config={"displayModeBar": False, "scrollZoom": False})
                st.caption("Uma associação entre variáveis não demonstra causa e efeito. Células vazias indicam correlação indefinida, por exemplo em variáveis constantes.")

with dashboard2:
    st.header("Perfil da amostra")
    st.write("Escolha um grupo e explore seu perfil. Estes filtros são independentes do Dashboard 1.")
    limites_idade = (float(df["Age"].min()), float(df["Age"].max()))
    if "d2_versao_selecao" not in st.session_state:
        st.session_state["d2_versao_selecao"] = 0

    def limpar_selecao():
        # Um novo gráfico limpa o evento, que é somente leitura no Streamlit.
        st.session_state["d2_versao_selecao"] += 1

    def limpar_filtros():
        st.session_state["d2_genero"] = "Todos"
        st.session_state["d2_idade"] = limites_idade
        st.session_state["d2_historico"] = "Todos"
        limpar_selecao()

    with st.container(border=True):
        filtro_genero, filtro_idade, filtro_historico, filtro_limpar = st.columns([1, 1.5, 1.3, 1])
        with filtro_genero:
            genero = st.selectbox("Gênero", ["Todos", "Feminino", "Masculino"],
                key="d2_genero", on_change=limpar_selecao)
        with filtro_idade:
            if limites_idade[0] == limites_idade[1]:
                idade = limites_idade
                st.caption(f"Idade única: {idade[0]:g} anos")
            else:
                idade = st.slider("Idade (anos)", min_value=limites_idade[0],
                    max_value=limites_idade[1],
                    value=None if "d2_idade" in st.session_state else limites_idade, step=0.01,
                    key="d2_idade", on_change=limpar_selecao)
        with filtro_historico:
            historico = st.selectbox("Histórico familiar de sobrepeso", ["Todos", "Sim", "Não"],
                key="d2_historico", on_change=limpar_selecao)
        with filtro_limpar:
            st.button("Limpar filtros", key="d2_limpar", on_click=limpar_filtros)

    dados_perfil = filtrar_perfil(df, genero, idade, historico)
    # Reservar o espaço permite exibir as métricas acima dos gráficos,
    # usando o evento de seleção retornado na mesma execução.
    area_metricas = st.container()
    area_contagem = st.empty()
    if dados_perfil.empty:
        dados_selecionados = dados_perfil
        st.info("Nenhum participante neste grupo. Amplie os filtros ou clique em Limpar filtros.")
    else:
        st.caption("Arraste uma região na dispersão para atualizar as métricas e as barras. Dê duplo clique no gráfico para remover a seleção.")
        coluna_barras, coluna_dispersao = st.columns(2)
        with coluna_barras:
            st.subheader("Categorias de peso")
            area_barras = st.empty()
        with coluna_dispersao:
            st.subheader("Idade × peso")
            evento = st.altair_chart(criar_dispersao(dados_perfil), width="stretch",
                key=f"d2_dispersao_{st.session_state['d2_versao_selecao']}",
                on_select="rerun", selection_mode=["recorte"])
        selecao = evento["selection"].get("recorte", {})
        dados_selecionados = aplicar_selecao(dados_perfil, selecao)
        with area_barras.container():
            st.altair_chart(criar_barras(dados_selecionados), width="stretch", key="d2_barras")
        if dados_selecionados.empty:
            st.info("Nenhum participante na região selecionada. Dê duplo clique na dispersão para limpar a seleção.")

    metricas = calcular_metricas(dados_selecionados)
    with area_metricas:
        cartoes = st.columns(4)
        cartoes[0].metric("Participantes", str(metricas["participantes"]))
        for cartao, titulo, chave, unidade in zip(cartoes[1:],
            ["Obeso no recorte (%)", "Idade média (anos)", "Peso médio (kg)"],
            ["percentual_obeso", "idade_media", "peso_medio"], ["%", "", ""]):
            valor = metricas[chave]
            texto = "—" if valor is None else f"{valor:.1f}{unidade}".replace(".", ",")
            cartao.metric(titulo, texto)
    area_contagem.caption(f"{len(dados_perfil)} participantes após os filtros · {len(dados_selecionados)} no recorte das métricas.")
    st.caption("Percentual referente a esta base, que inclui registros sintéticos. Não Obeso também inclui categorias diferentes de peso normal.")
