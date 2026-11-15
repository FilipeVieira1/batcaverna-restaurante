// Gerenciamento de menu mobile com acessibilidade e suporte a fechamento por tecla ESC
document.addEventListener("DOMContentLoaded", () => {
  const botao = document.querySelector(".menu-btn");
  const menu = document.getElementById("menu");
  if (!botao || !menu) return;

  const toggleMenu = (forcarEstado) => {
    const aberto = typeof forcarEstado === "boolean" ? forcarEstado : !menu.classList.contains("aberto");
    menu.classList.toggle("aberto", aberto);
    botao.setAttribute("aria-expanded", String(aberto));
  };

  botao.addEventListener("click", () => toggleMenu());

  // Fecha o menu ao redimensionar para telas maiores
  window.addEventListener("resize", () => {
    if (window.innerWidth > 768) {
      toggleMenu(false);
    }
  });

  // Fecha com a tecla Esc
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && menu.classList.contains("aberto")) {
      toggleMenu(false);
      botao.focus();
    }
  });
});