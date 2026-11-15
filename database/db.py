"""Acesso ao SQLite. Todas as consultas usam parâmetros (?), nunca texto concatenado."""
import sqlite3
from contextlib import closing
from pathlib import Path

BASE = Path(__file__).resolve().parent


def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row          # permite acessar colunas pelo nome
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path):
    """Cria as tabelas e, se o banco estiver vazio, carrega os dados fictícios."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with closing(get_connection(db_path)) as conn:
        conn.executescript((BASE / "schema.sql").read_text(encoding="utf-8"))
        vazio = conn.execute("SELECT COUNT(*) FROM Categoria").fetchone()[0] == 0
        if vazio:
            conn.executescript((BASE / "seed.sql").read_text(encoding="utf-8"))
        conn.commit()


def itens_disponiveis(db_path):
    """Retorna {categoria: [itens]} somente com itens disponíveis."""
    with closing(get_connection(db_path)) as conn:
        linhas = conn.execute(
            """SELECT i.item_id, i.nome, i.descricao, i.preco, c.nome AS categoria
               FROM ItemCardapio i JOIN Categoria c ON c.categoria_id = i.categoria_id
               WHERE i.disponivel = ?
               ORDER BY c.nome, i.nome""",
            (1,),
        ).fetchall()
    agrupado = {}
    for linha in linhas:
        agrupado.setdefault(linha["categoria"], []).append(linha)
    return agrupado


def catalogo_disponivel(db_path):
    """{item_id: {nome, preco}} dos itens disponíveis. O carrinho usa estes preços,
    nunca valores vindos do navegador."""
    with closing(get_connection(db_path)) as conn:
        linhas = conn.execute(
            "SELECT item_id, nome, preco FROM ItemCardapio WHERE disponivel = ?", (1,)
        ).fetchall()
    return {str(l["item_id"]): {"nome": l["nome"], "preco": l["preco"]} for l in linhas}
