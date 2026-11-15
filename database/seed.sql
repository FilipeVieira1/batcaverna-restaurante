INSERT INTO Categoria (nome, descricao) VALUES
  ('Pratos principais', ''),
  ('Porções', ''),
  ('Bebidas', '');
INSERT INTO ItemCardapio (nome, descricao, preco, disponivel, categoria_id) VALUES
  ('Prato 1', 'Descrição do prato.', 32.90, 1, 1),
  ('Prato 2', 'Descrição do prato.', 38.50, 1, 1),
  ('Prato 3 (indisponível)', 'Não deve aparecer no cardápio.', 45.00, 0, 1),
  ('Porção', 'Descrição da porção.', 27.00, 1, 2),
  ('Refrigerante', 'Lata 350 ml.', 6.50, 1, 3),
  ('Suco', 'Descrição da bebida.', 9.00, 1, 3);
