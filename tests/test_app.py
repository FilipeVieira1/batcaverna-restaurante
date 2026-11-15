import os, sqlite3, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app, formatar_preco


class TestBatcaverna(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.dir.name, "t.db")
        self.client = create_app(self.db).test_client()

    def tearDown(self):
        self.dir.cleanup()

    def pagina(self, rota):
        return self.client.get(rota).get_data(as_text=True)

    def test_paginas_e_navegacao(self):
        for rota in ("/", "/cardapio", "/contato"):
            html = self.pagina(rota)
            self.assertIn("Batcaverna", html)
            for destino in ('href="/"', 'href="/cardapio"', 'href="/contato"'):
                self.assertIn(destino, html)

    def test_cardapio_do_banco_com_preco_brl(self):
        html = self.pagina("/cardapio")
        for trecho in ("Prato 1", "R$ 32,90", "Pratos principais"):
            self.assertIn(trecho, html)
        for termo in ("exemplo", "fictício", "ficticio"):
            self.assertNotIn(termo, html.lower())

    def test_indisponivel_nao_aparece(self):
        self.assertNotIn("indisponível)", self.pagina("/cardapio"))

    def test_mensagem_sem_produtos(self):
        with sqlite3.connect(self.db) as c:
            c.execute("UPDATE ItemCardapio SET disponivel = 0")
        self.assertIn("Não há produtos disponíveis", self.pagina("/cardapio"))

    def test_links_contato(self):
        html = self.pagina("/contato")
        for trecho in ("https://wa.me/5511982917313", "google.com/maps",
                       "https://batcaverna.byfood.com.br/", "(11) 98291-7313"):
            self.assertIn(trecho, html)

    def test_escape_html(self):
        with sqlite3.connect(self.db) as c:
            c.execute("UPDATE ItemCardapio SET nome = '<script>x</script>' WHERE item_id = 1")
        self.assertNotIn("<script>x</script>", self.pagina("/cardapio"))

    def test_sem_rotas_de_escrita(self):
        for metodo in ("post", "put", "delete"):
            self.assertEqual(getattr(self.client, metodo)("/cardapio").status_code, 405)

    def test_404_amigavel(self):
        r = self.client.get("/nao-existe")
        self.assertEqual(r.status_code, 404)
        self.assertNotIn("Traceback", r.get_data(as_text=True))

    def test_inicio_destaques_do_banco(self):
        html = self.pagina("/")
        for trecho in ("Destaques do cardápio", "Pratos principais", "A partir de R$ 32,90",
                       "Rua Nelson Ezequiel de Farias", "Continue por aqui"):
            self.assertIn(trecho, html)
        self.assertNotIn("indisponível)", html)

    def test_links_de_continuidade(self):
        self.assertIn('href="/contato"', self.pagina("/cardapio").split("Continue por aqui")[1])
        self.assertIn('href="/cardapio"', self.pagina("/contato").split("Continue por aqui")[1])

    def test_formato_preco(self):
        self.assertEqual(formatar_preco(1234.5), "R$ 1.234,50")

    def test_restricoes_do_banco(self):
        with sqlite3.connect(self.db) as c:
            with self.assertRaises(sqlite3.IntegrityError):
                c.execute("INSERT INTO ItemCardapio (nome,preco,disponivel,categoria_id) VALUES ('x',0,1,1)")


if __name__ == "__main__":
    unittest.main()
