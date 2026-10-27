import pandas as pd
import streamlit as st


@st.cache_data(max_entries=64, show_spinner=False)
def calcular_correlacao(dados: pd.DataFrame) -> pd.DataFrame:
    """Cache por conteúdo: cada recorte e conjunto de colunas gera sua matriz."""
    return dados.corr(method="spearman")
