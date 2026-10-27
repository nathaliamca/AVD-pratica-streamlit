"""Recortes, métricas e gráficos do perfil da amostra."""
import altair as alt
import pandas as pd

CATEGORIAS = {
    "Insufficient_Weight": "Peso insuficiente",
    "Normal_Weight": "Peso normal",
    "Overweight_Level_I": "Sobrepeso I",
    "Overweight_Level_II": "Sobrepeso II",
    "Obesity_Type_I": "Obesidade I",
    "Obesity_Type_II": "Obesidade II",
    "Obesity_Type_III": "Obesidade III",
}


def filtrar_perfil(dados, genero, idade, historico):
    mascara = dados["Age"].between(*idade)
    if genero != "Todos":
        mascara &= dados["Gender"].eq({"Feminino": "Female", "Masculino": "Male"}[genero])
    if historico != "Todos":
        mascara &= dados["family_history_with_overweight"].eq({"Sim": "yes", "Não": "no"}[historico])
    return dados.loc[mascara].copy()


def aplicar_selecao(dados, selecao):
    """O intervalo Altair retorna limites por campo (Age e Weight)."""
    recorte = dados
    for coluna in ("Age", "Weight"):
        limites = selecao.get(coluna)
        if limites is not None and len(limites) == 2:
            recorte = recorte.loc[recorte[coluna].between(min(limites), max(limites))]
    return recorte


def calcular_metricas(dados):
    n = len(dados)
    return {
        "participantes": n,
        "percentual_obeso": 100 * dados["status_obesidade"].eq("Obeso").sum() / n if n else None,
        "idade_media": dados["Age"].mean() if n and dados["Age"].notna().any() else None,
        "peso_medio": dados["Weight"].mean() if n and dados["Weight"].notna().any() else None,
    }


def contar_categorias(dados):
    contagens = dados["NObeyesdad"].value_counts().reindex(CATEGORIAS, fill_value=0)
    return pd.DataFrame({"Categoria": list(CATEGORIAS.values()), "Participantes": contagens.to_numpy()})


def criar_dispersao(dados):
    selecao = alt.selection_interval(name="recorte", encodings=["x", "y"])
    pontos = dados[["Age", "Weight", "NObeyesdad", "status_obesidade"]].copy()
    pontos["Categoria"] = pontos["NObeyesdad"].map(CATEGORIAS)
    return (
        alt.Chart(pontos)
        .mark_circle(size=55)
        .encode(
            x=alt.X("Age:Q", title="Idade (anos)", scale=alt.Scale(zero=False)),
            y=alt.Y("Weight:Q", title="Peso (kg)", scale=alt.Scale(zero=False)),
            color=alt.Color("status_obesidade:N", title="Status de obesidade",
                scale=alt.Scale(domain=["Obeso", "Não Obeso"], range=["#6A3D78", "#ED6A5A"])),
            opacity=alt.condition(selecao, alt.value(0.8), alt.value(0.15)),
            tooltip=[alt.Tooltip("Age:Q", title="Idade", format=".1f"),
                alt.Tooltip("Weight:Q", title="Peso (kg)", format=".1f"),
                alt.Tooltip("status_obesidade:N", title="Status"),
                alt.Tooltip("Categoria:N", title="Categoria")],
        )
        .add_params(selecao)
        .properties(height=340)
    )


def criar_barras(dados):
    return (
        alt.Chart(contar_categorias(dados)).mark_bar(color="#C74736")
        .encode(
            x=alt.X("Participantes:Q", title="Participantes", axis=alt.Axis(tickMinStep=1)),
            y=alt.Y("Categoria:N", sort=list(CATEGORIAS.values()), title=None),
            tooltip=["Categoria:N", "Participantes:Q"],
        )
        .properties(height=340)
    )
