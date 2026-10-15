import tempfile
import unittest
from pathlib import Path

import fitz

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import destacador_boletins_v3_2_1 as app


class DestacadorBoletinsTests(unittest.TestCase):
    def criar_boletim(self, page, y, nome, notas, faltas):
        # Layout sintético baseado nas coordenadas de coluna usadas pelo aplicativo.
        page.insert_text((35, y), f"Nome: {nome}", fontsize=10)
        page.insert_text((35, y + 30), "Disciplina", fontsize=10)

        for x in (150, 223, 296):
            page.insert_text((x, y + 40), "Nota", fontsize=9)

        for x, nota in zip((152, 225, 298), notas):
            page.insert_text((x, y + 60), f"{nota:.1f}", fontsize=9)

        for x, falta in zip((193, 267, 340), faltas):
            page.insert_text((x, y + 60), str(falta), fontsize=9)

        page.insert_text((35, y + 130), "Resultado", fontsize=10)

    def test_dois_boletins_na_mesma_folha(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pasta = Path(temp_dir)
            entrada = pasta / "boletins_ficticios.pdf"
            saida = pasta / "boletins_processados.pdf"
            relatorio = pasta / "relatorio.pdf"

            doc = fitz.open()
            page = doc.new_page(width=595, height=842)
            self.criar_boletim(page, 100, "Aluno Um", (5.0, 8.0, 9.0), (1, 2, 3))
            self.criar_boletim(page, 400, "Aluno Dois", (8.0, 9.0, 9.0), (0, 1, 2))
            doc.save(entrada)
            doc.close()

            marcadas, alunos, alunos_com_notas_baixas = app.processar(
                str(entrada), str(saida), str(relatorio)
            )

            self.assertTrue(saida.exists())
            self.assertTrue(relatorio.exists())
            self.assertEqual(len(alunos), 2, "deve identificar os dois boletins da página")
            self.assertEqual(alunos_com_notas_baixas, 1)
            self.assertGreaterEqual(marcadas, 1, "a nota 5,0 deve ser contornada")

            with fitz.open(saida) as processado:
                texto = processado[0].get_text()
                self.assertEqual(texto.count("Aproveitamento:"), 2)
                self.assertIn("Total de faltas: 6", texto)
                self.assertIn("Total de faltas: 3", texto)
                self.assertGreaterEqual(
                    len(list(processado[0].annots() or [])), 1,
                    "a nota baixa deve estar marcada no PDF de saída"
                )
                self.assertGreaterEqual(
                    len(processado[0].get_drawings()), 3,
                    "devem existir estrelas desenhadas para os dois boletins"
                )

            with fitz.open(relatorio) as ficha:
                texto_relatorio = ficha[0].get_text()
                self.assertIn("Aluno(a): Aluno Um", texto_relatorio)
                self.assertNotIn("Aluno(a): Aluno Dois", texto_relatorio)

    def test_faixas_de_classificacao(self):
        self.assertEqual(app.classificar(96), "Avançado")
        self.assertEqual(app.classificar(95), "Adequado")
        self.assertEqual(app.classificar(81), "Adequado")
        self.assertEqual(app.classificar(80), "Básico")
        self.assertEqual(app.classificar(61), "Básico")
        self.assertEqual(app.classificar(60), "Abaixo do básico")


if __name__ == "__main__":
    unittest.main()
