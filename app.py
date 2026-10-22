import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(page_title="Análise de obesidade", layout="wide")
st.title("Obesidade: explorando os dados")
df = load_data()

VARS_QUANT = ["Age", "Height", "Weight", "FCVC", "NCP", "CH2O", "FAF", "TUE"]
NOMES = {
    "Age": "Idade (anos)", "Height": "Altura (m)", "Weight": "Peso (kg)",
    "FCVC": "Consumo de vegetais", "NCP": "Refeições principais",
    "CH2O": "Consumo de água", "FAF": "Atividade física",
    "TUE": "Uso de dispositivos eletrônicos",
}

with st.sidebar:
    st.header("Filtros")
    variaveis = st.multiselect(
        "Variáveis da análise", options=VARS_QUANT, default=VARS_QUANT,
        format_func=lambda nome: NOMES.get(nome, nome),
    )
    separar_por_classe = st.toggle("Comparar por status de obesidade", value=False)
    intervalos = {}
    for var in variaveis:
        if pd.api.types.is_integer_dtype(df[var]):
            minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
        else:
            minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.01
        if minimo == maximo:
            intervalos[var] = (minimo, maximo)
            continue
        intervalos[var] = st.slider(
            f"Intervalo: {NOMES[var]}", min_value=minimo, max_value=maximo,
            value=(minimo, maximo), step=passo, key=f"intervalo_{var}",
        )

df_filtrado = df
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]
st.caption(f"{len(df_filtrado)} de {len(df)} participantes dentro dos intervalos escolhidos.")

if not variaveis:
    st.info("Selecione uma ou mais variáveis na lateral para começar.")
elif df_filtrado.empty:
    st.info("Nenhum participante neste recorte. Amplie os intervalos na lateral.")
else:
    distribuicao, correlacao = st.tabs(["Distribuição", "Relações entre variáveis"])
    with distribuicao:
        st.subheader("Como os valores se distribuem?")
        # TODO Aula 22: seletor da variável e histograma por status_obesidade.
    with correlacao:
        st.subheader("Quais medidas variam juntas?")
        if len(variaveis) < 2:
            st.info("Selecione ao menos duas variáveis para calcular a correlação.")
        # TODO Aula 22: calcular e apresentar a matriz de correlação.
