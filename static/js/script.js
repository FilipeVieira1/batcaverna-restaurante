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
// ===== Carrinho simples =====
// Guarda só {id: quantidade} no navegador. Nomes e preços vêm sempre do servidor (/api/itens).
(() => {
  const CHAVE = "batcaverna_carrinho", MAX = 20;
  const brl = (v) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
  const ler = () => { try { const o = JSON.parse(localStorage.getItem(CHAVE) || "{}"); return o && typeof o === "object" ? o : {}; } catch { return {}; } };
  const gravar = (c) => { try { localStorage.setItem(CHAVE, JSON.stringify(c)); } catch { /* armazenamento indisponível */ } };
  const total = (c) => Object.values(c).reduce((s, q) => s + (Number(q) || 0), 0);
  const selo = () => { const e = document.getElementById("carrinho-qtd"); if (e) e.textContent = total(ler()); };

  document.addEventListener("DOMContentLoaded", () => {
    selo();
    const sec = document.getElementById("carrinho");
    const $ = (id) => document.getElementById(id);
    let catalogo = {};

    const render = () => {
      if (!sec) { selo(); return; }
      const carrinho = ler(), lista = $("carrinho-lista");
      lista.replaceChildren();
      let soma = 0; const linhas = [];
      for (const [id, q] of Object.entries(carrinho)) {
        const item = catalogo[id], qtd = Math.min(MAX, Math.max(1, parseInt(q, 10) || 0));
        if (!item) { delete carrinho[id]; continue; }          // item sumiu/indisponível
        const sub = item.preco * qtd; soma += sub; linhas.push(`${qtd}x ${item.nome} - ${brl(sub)}`);
        const li = document.createElement("li");
        const nome = document.createElement("span"); nome.textContent = `${item.nome} · ${brl(sub)}`;
        const ctrl = document.createElement("span"); ctrl.className = "qtd";
        const mk = (txt, rot, delta) => { const b = document.createElement("button"); b.type = "button"; b.textContent = txt; b.setAttribute("aria-label", `${rot} ${item.nome}`); b.addEventListener("click", () => alterar(id, delta)); return b; };
        const n = document.createElement("span"); n.textContent = qtd;
        ctrl.append(mk("−", "Diminuir", -1), n, mk("+", "Aumentar", 1));
        li.append(nome, ctrl); lista.append(li);
      }
      gravar(carrinho); selo();
      const vazio = linhas.length === 0;
      $("carrinho-vazio").hidden = !vazio; $("carrinho-total").hidden = vazio; $("carrinho-acoes").hidden = vazio;
      $("carrinho-total").textContent = `Total: ${brl(soma)}`;
      const msg = `Olá! Gostaria de fazer um pedido:\n${linhas.join("\n")}\nTotal: ${brl(soma)}`;
      $("carrinho-enviar").href = `${sec.dataset.whatsapp}?text=${encodeURIComponent(msg)}`;
    };
    const alterar = (id, delta) => {
      const c = ler(); const nova = (parseInt(c[id], 10) || 0) + delta;
      if (nova <= 0) delete c[id]; else c[id] = Math.min(MAX, nova);
      gravar(c); render();
    };

    const feedbackTimers = new WeakMap();
    document.querySelectorAll(".add-carrinho").forEach((b) => {
      const rotuloOriginal = b.textContent;
      b.addEventListener("click", () => {
        alterar(b.dataset.id, 1);
        const av = $("carrinho-aviso"); if (av) av.textContent = `${b.getAttribute("aria-label").replace("Adicionar ", "").replace(" ao carrinho", "")} adicionado ao carrinho.`;
        const timerAnterior = feedbackTimers.get(b);
        if (timerAnterior !== undefined) window.clearTimeout(timerAnterior);
        b.classList.add("adicionado");
        b.textContent = "Adicionado ✓";
        feedbackTimers.set(b, window.setTimeout(() => {
          b.classList.remove("adicionado");
          b.textContent = rotuloOriginal;
          feedbackTimers.delete(b);
        }, 1400));
      });
    });
    if (sec) $("carrinho-limpar").addEventListener("click", () => { gravar({}); render(); });

    if (sec) fetch(sec.dataset.api).then((r) => r.json()).then((d) => { catalogo = d; render(); }).catch(() => { $("carrinho-vazio").textContent = "Não foi possível carregar o carrinho agora."; });
  });
})();
