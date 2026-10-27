import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data(ttl=300, max_entries=8, show_spinner=False)
def load_data(path="data/clean/dataset.csv"):
    """Lê o CSV tratado e reutiliza o resultado por até cinco minutos."""
    arquivo = Path(path)
    if not arquivo.is_absolute():
        arquivo = Path(__file__).resolve().parents[1] / arquivo
    return pd.read_csv(arquivo)
