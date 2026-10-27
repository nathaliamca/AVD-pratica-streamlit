import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_data
from src.dashboard1 import calcular_correlacao


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
