import unittest
import requests
import sys
import os

# Adiciona o diretório 'src' ao caminho do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import cdi

class TestCDIFunction(unittest.TestCase):

    def test_cdi(self):
        data_inicial = "14/08/2023"
        data_final = "18/08/2023"

        resultados = cdi.cdi(data_inicial, data_final)

        # Verificar se a lista não está vazia
        self.assertTrue(resultados, f"Erro: Nenhum registro retornado para o intervalo {data_inicial} - {data_final}")

        # Verificar se as datas de teste estão nos resultados
        datas_retornadas = [registro['data'] for registro in resultados]
        self.assertIn(data_inicial, datas_retornadas, f"Erro: Data {data_inicial} não encontrada nos resultados")
        self.assertIn(data_final, datas_retornadas, f"Erro: Data {data_final} não encontrada nos resultados")

if __name__ == "__main__":
    unittest.main()
