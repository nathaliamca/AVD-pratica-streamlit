import json
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pyarrow as pa
import streamlit as st
from streamlit.testing.v1 import AppTest

from src.dashboard2 import (filtrar_perfil, aplicar_selecao, calcular_metricas,
    contar_categorias, criar_dispersao, criar_barras)

APP = str(Path(__file__).resolve().parents[1] / "app.py")


class Dashboard2Tests(unittest.TestCase):
    def setUp(self):
        self.dados = pd.read_csv("data/clean/dataset.csv")

    def test_calculos_recorte_e_categorias(self):
        dados = filtrar_perfil(self.dados, "Feminino", (20, 30), "Não")
        esperado = self.dados.loc[
            self.dados.Gender.eq("Female") & self.dados.Age.between(20, 30)
            & self.dados.family_history_with_overweight.eq("no")]
        pd.testing.assert_frame_equal(dados, esperado)
        recorte = aplicar_selecao(dados, {"Age": [22, 28], "Weight": [50, 90]})
        esperado = esperado.loc[esperado.Age.between(22, 28) & esperado.Weight.between(50, 90)]
        pd.testing.assert_frame_equal(recorte, esperado)
        metricas = calcular_metricas(recorte)
        self.assertEqual(metricas["participantes"], len(esperado))
        self.assertAlmostEqual(metricas["percentual_obeso"], esperado.status_obesidade.eq("Obeso").mean() * 100)
        self.assertAlmostEqual(metricas["peso_medio"], esperado.Weight.mean())
        self.assertAlmostEqual(metricas["idade_media"], esperado.Age.mean())
        barras = contar_categorias(recorte)
        self.assertEqual(len(barras), 7)
        self.assertEqual(barras.Participantes.sum(), len(recorte))

    def test_vazio_e_sem_valores_validos(self):
        vazio = self.dados.iloc[:0]
        self.assertEqual(calcular_metricas(vazio), {"participantes": 0,
            "percentual_obeso": None, "idade_media": None, "peso_medio": None})
        self.assertEqual(contar_categorias(vazio).Participantes.sum(), 0)
        dados = self.dados.iloc[:1].assign(Age=float("nan"), Weight=float("nan"))
        self.assertIsNone(calcular_metricas(dados)["idade_media"])
        self.assertIsNone(calcular_metricas(dados)["peso_medio"])
        pd.testing.assert_frame_equal(aplicar_selecao(self.dados, {}), self.dados)

    def test_especificacoes_altair(self):
        dispersao = criar_dispersao(self.dados).to_dict()
        barras = criar_barras(self.dados).to_dict()
        self.assertEqual(dispersao["params"][0]["name"], "recorte")
        self.assertEqual(dispersao["params"][0]["select"]["type"], "interval")
        self.assertEqual(barras["mark"]["type"], "bar")

    def test_widgets_metricas_reset_e_independencia(self):
        app = AppTest.from_file(APP, default_timeout=30).run()
        self.assertFalse(app.exception)
        self.assertEqual([t.label for t in app.tabs if t.label.startswith("Dashboard")], ["Dashboard 1", "Dashboard 2"])
        self.assertEqual(app.metric[0].value, str(len(self.dados)))
        app.selectbox(key="d2_genero").set_value("Feminino").run()
        app.selectbox(key="d2_historico").set_value("Não").run()
        app.slider(key="d2_idade").set_value((20.0, 30.0)).run()
        esperado = filtrar_perfil(self.dados, "Feminino", (20, 30), "Não")
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, str(len(esperado)))
        self.assertEqual(app.metric[3].value, f"{esperado.Weight.mean():.1f}".replace(".", ","))
        # Alterar o Dashboard 1 não modifica o recorte do Dashboard 2.
        app.multiselect[0].set_value([]).run()
        self.assertEqual(app.metric[0].value, str(len(esperado)))
        app.slider(key="d2_idade").set_value((60.0, 60.0)).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, "0")
        self.assertEqual(app.metric[1].value, "—")
        app.button(key="d2_limpar").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, str(len(self.dados)))
        self.assertEqual(app.selectbox(key="d2_genero").value, "Todos")

    def test_evento_de_selecao_atualiza_metricas_e_barras(self):
        # Simular o payload retornado pelo gráfico. O gesto no navegador
        # não é exercitado pelo AppTest; a integração Python é verificada aqui.
        original = st.altair_chart
        selecao = {"Age": [20, 25], "Weight": [60, 85]}

        def retornar_evento(chart, **kwargs):
            resultado = original(chart, **kwargs)
            return {"selection": {"recorte": selecao}} if kwargs.get("on_select") == "rerun" else resultado

        with patch("streamlit.altair_chart", side_effect=retornar_evento):
            app = AppTest.from_file(APP, default_timeout=30).run()
        self.assertFalse(app.exception)
        esperado = aplicar_selecao(self.dados, selecao)
        self.assertEqual(app.metric[0].value, str(len(esperado)))
        self.assertEqual(app.metric[2].value, f"{esperado.Age.mean():.1f}".replace(".", ","))
        graficos = app.get("vega_lite_chart")
        self.assertEqual(len(graficos), 2)
        grafico_barras = next(g for g in graficos if json.loads(g.proto.spec).get("mark", {}).get("type") == "bar")
        spec = json.loads(grafico_barras.proto.spec)
        self.assertEqual(spec["mark"]["type"], "bar")
        dados_barras = pa.ipc.open_stream(grafico_barras.proto.datasets[0].data.data).read_all().to_pandas()
        pd.testing.assert_frame_equal(dados_barras.reset_index(drop=True), contar_categorias(esperado))


if __name__ == "__main__":
    unittest.main()
