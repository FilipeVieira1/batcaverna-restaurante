-- ATENÇÃO: DADOS FICTÍCIOS DE DEMONSTRAÇÃO.
-- Substitua pelos itens e preços reais fornecidos pelo restaurante (veja o README).
INSERT INTO Categoria (nome, descricao) VALUES
  ('Pratos principais', 'Exemplo de categoria'),
  ('Porções', 'Exemplo de categoria'),
  ('Bebidas', 'Exemplo de categoria');
INSERT INTO ItemCardapio (nome, descricao, preco, disponivel, categoria_id) VALUES
  ('Prato exemplo 1', 'Descrição fictícia do prato.', 32.90, 1, 1),
  ('Prato exemplo 2', 'Descrição fictícia do prato.', 38.50, 1, 1),
  ('Prato exemplo 3 (indisponível)', 'Não deve aparecer no cardápio.', 45.00, 0, 1),
  ('Porção exemplo', 'Descrição fictícia da porção.', 27.00, 1, 2),
  ('Refrigerante exemplo', 'Lata 350 ml (fictício).', 6.50, 1, 3),
  ('Suco exemplo', 'Descrição fictícia da bebida.', 9.00, 1, 3);
