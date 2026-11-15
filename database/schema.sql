-- Esquema do banco do Batcaverna Restaurante
CREATE TABLE IF NOT EXISTS Categoria (
    categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL UNIQUE,
    descricao    TEXT
);
CREATE TABLE IF NOT EXISTS ItemCardapio (
    item_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL,
    descricao    TEXT,
    preco        REAL NOT NULL CHECK (preco > 0),
    disponivel   INTEGER NOT NULL DEFAULT 1 CHECK (disponivel IN (0, 1)),
    categoria_id INTEGER NOT NULL REFERENCES Categoria (categoria_id)
);
CREATE INDEX IF NOT EXISTS idx_item_categoria ON ItemCardapio (categoria_id, disponivel);
