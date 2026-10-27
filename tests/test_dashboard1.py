"""Execute: python -m unittest discover -s tests -v."""
import base64
import json
import unittest
from unittest.mock import patch
from pathlib import Path

import numpy as np
import pandas as pd
from streamlit.testing.v1 import AppTest

from src.data_loader import load_data
from src.dashboard1 import calcular_correlacao


def valores_plotly(valor):
    if isinstance(valor, dict) and "bdata" in valor:
        vetor = np.frombuffer(base64.b64decode(valor["bdata"]), dtype=valor["dtype"])
        if "shape" in valor:
            vetor = vetor.reshape(tuple(map(int, valor["shape"].split(","))))
        return vetor
    return np.asarray(valor, dtype=float)


class Dashboard1Tests(unittest.TestCase):
    def setUp(self):
        self.dados = pd.read_csv("data/clean/dataset.csv")
        self.app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=30).run()
        self.sem_erros()

    def sem_erros(self):
        self.assertEqual(len(self.app.exception), 0)

    def graficos(self):
        return [json.loads(item.proto.spec) for item in self.app.get("plotly_chart")]

    def test_zero_uma_e_duas_variaveis(self):
        self.app.multiselect[0].set_value([]).run()
        self.sem_erros()
        self.assertEqual(len(self.graficos()), 0)
        self.assertIn("Selecione", self.app.info[0].value)
        self.app.multiselect[0].set_value(["Weight"]).run()
        self.sem_erros()
        self.assertEqual(len(self.graficos()), 1)
        self.assertEqual(self.app.selectbox[0].value, "Weight")
        self.app.multiselect[0].set_value(["Age", "Weight"]).run()
        self.sem_erros()
        self.assertEqual(len(self.graficos()), 2)

    def test_filtros_recalculam_dados_e_correlacao(self):
        self.app.multiselect[0].set_value(["Age", "Weight"]).run()
        for intervalo in [(20.0, 30.0), (30.0, 45.0)]:
            self.app.slider(key="intervalo_Age").set_value(intervalo).run()
            self.app.slider(key="intervalo_Weight").set_value((60.0, 100.0)).run()
            self.sem_erros()
            esperado = self.dados[
                self.dados.Age.between(*intervalo) & self.dados.Weight.between(60, 100)
            ]
            hist, corr = self.graficos()
            np.testing.assert_allclose(valores_plotly(hist["data"][0]["x"]), esperado.Age)
            np.testing.assert_allclose(
                valores_plotly(corr["data"][0]["z"]),
                esperado[["Age", "Weight"]].corr(method="spearman"),
                equal_nan=True,
            )
            self.assertTrue(any(c.value.startswith(f"{len(esperado)} de") for c in self.app.caption))
        self.app.toggle[0].set_value(True).run()
        self.sem_erros()
        hist = self.graficos()[0]
        self.assertEqual({t["name"] for t in hist["data"]}, set(esperado.status_obesidade))
        for trace in hist["data"]:
            np.testing.assert_allclose(
                valores_plotly(trace["x"]),
                esperado.loc[esperado.status_obesidade == trace["name"], "Age"],
            )

    def test_remover_variavel_do_histograma(self):
        self.app.selectbox[0].set_value("Weight").run()
        self.app.multiselect[0].set_value(["Age", "Height"]).run()
        self.sem_erros()
        self.assertIn(self.app.selectbox[0].value, ["Age", "Height"])

    def test_recorte_vazio_e_recuperacao(self):
        self.app.multiselect[0].set_value(["Age", "Weight"]).run()
        self.app.slider(key="intervalo_Age").set_value((14.0, 14.0)).run()
        self.app.slider(key="intervalo_Weight").set_value((170.0, 173.0)).run()
        self.sem_erros()
        self.assertEqual(len(self.graficos()), 0)
        self.assertIn("Nenhum participante", self.app.info[0].value)
        self.app.slider(key="intervalo_Age").set_value((20.0, 40.0)).run()
        self.app.slider(key="intervalo_Weight").set_value((50.0, 120.0)).run()
        self.sem_erros()
        self.assertEqual(len(self.graficos()), 2)

    def test_um_participante_e_variavel_constante(self):
        for dados, quantidade_graficos in [(self.dados.iloc[:1], 1), (self.dados.iloc[:5].assign(Age=20.0), 2)]:
            with self.subTest(linhas=len(dados)), patch("src.data_loader.load_data", return_value=dados):
                self.app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=30).run()
                self.sem_erros()
                self.assertEqual(len(self.graficos()), quantidade_graficos)
                if len(dados) > 1:
                    matriz = valores_plotly(self.graficos()[1]["data"][0]["z"])
                    self.assertTrue(np.isnan(matriz[0]).all())

    def test_cache_reutiliza_csv_e_mantem_copias_independentes(self):
        load_data.clear()
        with patch("src.data_loader.pd.read_csv", return_value=self.dados.copy()) as leitura:
            primeiro = load_data()
            primeiro.loc[0, "Age"] = -1
            segundo = load_data()
            self.assertEqual(leitura.call_count, 1)
            self.assertNotEqual(segundo.loc[0, "Age"], -1)
        load_data.clear()
        calcular_correlacao.clear()


if __name__ == "__main__":
    unittest.main()
