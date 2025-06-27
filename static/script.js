let isLoggedIn = false;

window.onload = function () {
  carregarTabela("reagentes");
  carregarTabela("meios");
  carregarTabela("agenda");
};

function showTab(tabId) {
  document.querySelectorAll("section").forEach((s) => s.classList.remove("active"));
  document.getElementById(tabId).classList.add("active");
}

function toggleLogin() {
  const usuario = prompt("Usuário:");
  const senha = prompt("Senha:");

  if (usuario === "admin" && senha === "senha123") {
    isLoggedIn = true;
    document.getElementById("user-display").innerText = `Bem-vindo, ${usuario}`;
    document.getElementById("login-btn").classList.add("hidden");
    document.getElementById("logout-btn").classList.remove("hidden");
    document.querySelectorAll(".edit-only").forEach((e) => e.classList.remove("hidden"));
  } else {
    alert("Login inválido");
  }
}

function logout() {
  isLoggedIn = false;
  document.getElementById("user-display").innerText = "";
  document.getElementById("login-btn").classList.remove("hidden");
  document.getElementById("logout-btn").classList.add("hidden");
  document.querySelectorAll(".edit-only").forEach((e) => e.classList.add("hidden"));
}

async function carregarTabela(tabela) {
  const body = document.getElementById(`${tabela}-body`);
  body.innerHTML = "";

  const resposta = await fetch(`/api/${tabela}`);
  const dados = await resposta.json();

  dados.forEach((item) => {
    const linha = document.createElement("tr");
    linha.innerHTML = `
      <td>${item.nome || item.equipamento}</td>
      <td>${item.quantidade || item.usuario}</td>
      <td>${item.validade || item.data}</td>
      <td>${item.localizacao || item.horario}</td>
      <td class="edit-only hidden">
        <button onclick="editar(this, '${tabela}', ${item.id})">Editar</button>
        <button onclick="remover(this, '${tabela}', ${item.id})">Remover</button>
      </td>
    `;
    body.appendChild(linha);
  });
}

async function adicionar(tabela) {
  const nome = prompt("Nome/Equipamento:");
  const q1 = prompt("Quantidade/Usuário:");
  const q2 = prompt("Validade/Data:");
  const q3 = prompt("Localização/Horário:");

  if (!nome || !q1 || !q2 || !q3) return;

  const payload =
    tabela === "agenda"
      ? { equipamento: nome, usuario: q1, data: q2, horario: q3 }
      : { nome: nome, quantidade: q1, validade: q2, localizacao: q3 };

  const resposta = await fetch(`/api/${tabela}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (resposta.ok) carregarTabela(tabela);
  else alert("Erro ao adicionar item.");
}

async function editar(botao, tabela, id) {
  const row = botao.closest("tr");
  const colunas = row.querySelectorAll("td");

  const novo1 = prompt("Novo Nome/Equipamento:", colunas[0].innerText);
  const novo2 = prompt("Nova Quantidade/Usuário:", colunas[1].innerText);
  const novo3 = prompt("Nova Validade/Data:", colunas[2].innerText);
  const novo4 = prompt("Nova Localização/Horário:", colunas[3].innerText);

  if (!novo1 || !novo2 || !novo3 || !novo4) return;

  const payload =
    tabela === "agenda"
      ? { equipamento: novo1, usuario: novo2, data: novo3, horario: novo4 }
      : { nome: novo1, quantidade: novo2, validade: novo3, localizacao: novo4 };

  const resposta = await fetch(`/api/${tabela}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (resposta.ok) carregarTabela(tabela);
  else alert("Erro ao editar item.");
}

async function remover(botao, tabela, id) {
  if (!confirm("Tem certeza que deseja remover?")) return;

  const resposta = await fetch(`/api/${tabela}/${id}`, {
    method: "DELETE",
  });

  if (resposta.ok) carregarTabela(tabela);
  else alert("Erro ao remover item.");
}
