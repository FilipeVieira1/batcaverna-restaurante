"""Batcaverna Restaurante - aplicação Flask (rotas somente de leitura)."""
import os
from pathlib import Path
from urllib.parse import quote

from flask import Flask, jsonify, render_template
from werkzeug.exceptions import HTTPException

from database.db import catalogo_disponivel, init_db, itens_disponiveis

ENDERECO = "Rua Nelson Ezequiel de Farias, 231, Jardim Briquet, Itapevi-SP"
WHATSAPP_EXIBIDO = "(11) 98291-7313"
WHATSAPP_LINK = "https://wa.me/5511982917313"
PEDIDOS_URL = "https://batcaverna.byfood.com.br/"
MAPS_URL = "https://www.google.com/maps/search/?api=1&query=" + quote(ENDERECO)


def formatar_preco(valor):
    """32.9 -> 'R$ 32,90'"""
    texto = f"{float(valor):,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def create_app(db_path=None):
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path or os.environ.get(
        "BATCAVERNA_DB", str(Path(app.instance_path) / "batcaverna.db"))
    # Aviso de dados fictícios; defina BATCAVERNA_DEMO=0 ao usar dados reais.
    app.config["MODO_DEMO"] = os.environ.get("BATCAVERNA_DEMO", "1") == "1"
    app.jinja_env.filters["brl"] = formatar_preco
    init_db(app.config["DB_PATH"])

    @app.context_processor
    def globais():
        return dict(modo_demo=app.config["MODO_DEMO"], pedidos_url=PEDIDOS_URL)

    @app.get("/")
    def index():
        return render_template("index.html", categorias=itens_disponiveis(app.config["DB_PATH"]),
                               endereco=ENDERECO, whatsapp=WHATSAPP_EXIBIDO)

    @app.get("/cardapio")
    def cardapio():
        return render_template("cardapio.html",
                               categorias=itens_disponiveis(app.config["DB_PATH"]))

    @app.get("/carrinho")
    def carrinho():
        return render_template("carrinho.html", whatsapp_link=WHATSAPP_LINK)

    @app.get("/api/itens")
    def api_itens():
        """Catálogo (somente leitura) para o carrinho do navegador."""
        resposta = jsonify(catalogo_disponivel(app.config["DB_PATH"]))
        resposta.headers["Cache-Control"] = "no-store"
        return resposta

    @app.get("/contato")
    def contato():
        return render_template("contato.html", endereco=ENDERECO,
                               whatsapp=WHATSAPP_EXIBIDO, whatsapp_link=WHATSAPP_LINK,
                               maps_url=MAPS_URL)

    @app.errorhandler(404)
    def nao_encontrado(_):
        return render_template("erro.html", titulo="Página não encontrada",
                               msg="O endereço que você acessou não existe."), 404

    @app.errorhandler(Exception)
    def erro_interno(erro):
        if isinstance(erro, HTTPException):  # ex.: 405 mantém o código correto
            return render_template("erro.html", titulo="Requisição não permitida",
                                   msg="Esta ação não está disponível."), erro.code
        # Mensagem amigável: nenhum detalhe técnico é exibido ao visitante.
        return render_template("erro.html", titulo="Algo deu errado",
                               msg="Tente novamente em alguns instantes."), 500

    return app


app = create_app()

if __name__ == "__main__":
    # debug=False: nunca ative o modo debug em produção.
    app.run(host="127.0.0.1", port=5000, debug=False)
