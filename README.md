# Batcaverna Restaurante — site institucional (MVP acadêmico)

Flask 3 + SQLite + HTML/CSS/JS. Três telas: Início, Cardápio (lido do SQLite) e Localização e contato.
Sem login, painel admin ou rotas de escrita (por requisito).

## Executar localmente
```bash
python3.12 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                    # abra http://127.0.0.1:5000
```
O banco `instance/batcaverna.db` é criado automaticamente na primeira execução, com itens iniciais.

## Testes
```bash
python -m unittest discover -s tests -v
```

## Arquitetura (3 camadas)
- **Apresentação:** `templates/`, `static/css`, `static/js`
- **Aplicação:** `app.py` (rotas GET, filtro de preço R$, erros amigáveis)
- **Dados:** `database/` (`schema.sql`, `seed.sql`, `db.py` com consultas parametrizadas). O arquivo `.db` fica em `instance/`, fora de `static/`, portanto não é servido.

## Atualizar os itens do cardápio
1. Edite `database/seed.sql` com categorias, itens e preços reais (preço > 0; `disponivel` 1 ou 0).
2. Apague `instance/batcaverna.db` e rode `python app.py` de novo (o banco é recriado).
3. Em `templates/contato.html`, preencha os horários no campo marcado `PREENCHER`.

## Produção
Não use `app.run`. Exemplo: `pip install gunicorn && gunicorn app:app` (debug permanece desligado).

## Pendente de confirmação com o restaurante
Horários de funcionamento, cardápio e preços reais, logotipo/fotos oficiais e texto institucional definitivo.

## Estrutura de conteúdo (atualização)
- `templates/_continuar.html`: bloco de links de continuidade, reutilizado nas três páginas.
- A página inicial lê as categorias disponíveis do SQLite ("Destaques do cardápio"); nenhuma alteração no banco foi necessária.
- Todo texto institucional usa apenas informações confirmadas (nome, endereço, WhatsApp, plataforma de pedidos). Horários continuam pendentes.
