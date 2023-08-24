import unittest
import sys
import os

# Adiciona o diretório 'src' ao caminho do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import cdi

class TestCDIFunction(unittest.TestCase):

    def test_cdi(self):
        dia_teste = "20/08/2021"
        resultado = cdi.cdi(dia_teste)
        
        self.assertIsNotNone(resultado, f"Erro: Nenhum registro retornado para {dia_teste}")
        self.assertEqual(resultado['data'], dia_teste, f"Erro: Data retornada ({resultado['data']}) não corresponde à data fornecida ({dia_teste}")

if __name__ == "__main__":
    unittest.main()