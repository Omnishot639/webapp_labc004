let isLoggedIn = false;

    function showTab(tabId) {
      document.querySelectorAll('section').forEach(s => s.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
    }

    function toggleLogin() {
      const usuario = prompt("Usuário:");
      const senha = prompt("Senha:");

      if (usuario === "admin" && senha === "senha123") {
        isLoggedIn = true;
        document.getElementById("user-display").innerText = `Bem-vindo, ${usuario}`;
        document.getElementById("login-btn").classList.add("hidden");
        document.getElementById("logout-btn").classList.remove("hidden");
        document.querySelectorAll(".edit-only").forEach(e => e.classList.remove("hidden"));
      } else {
        alert("Login inválido");
      }
    }

    function logout() {
      isLoggedIn = false;
      document.getElementById("user-display").innerText = "";
      document.getElementById("login-btn").classList.remove("hidden");
      document.getElementById("logout-btn").classList.add("hidden");
      document.querySelectorAll(".edit-only").forEach(e => e.classList.add("hidden"));
    }

    function adicionar(tabela) {
      alert(`Função de adicionar item à tabela: ${tabela}`);
    }

    function adicionar(tabela) {
      const nome = prompt("Nome:");
      const quantidade = prompt("Quantidade:");
      const validade = prompt("Validade:");
      const local = prompt("Localização/Data/Horário:");

      if (!nome || !quantidade || !validade || !local) return;

      const tbody = document.getElementById(`${tabela}-body`);
      const novaLinha = document.createElement("tr");
      let colunas;

      if (tabela === 'agenda') {
        colunas = `<td>${nome}</td><td>${quantidade}</td><td>${validade}</td><td>${local}</td>`;
      } else {
        colunas = `<td>${nome}</td><td>${quantidade}</td><td>${validade}</td><td>${local}</td>`;
      }

      novaLinha.innerHTML = `${colunas}<td class="edit-only"><button onclick="editar(this)">Editar</button><button onclick="remover(this)">Remover</button></td>`;
      tbody.appendChild(novaLinha);
    }

    function editar(btn) {
      const row = btn.closest("tr");
      const tds = row.querySelectorAll("td");
      for (let i = 0; i < tds.length - 1; i++) {
        const novoValor = prompt(`Novo valor para ${tds[i].textContent}:`, tds[i].textContent);
        if (novoValor) tds[i].textContent = novoValor;
      }
    }

    function remover(btn) {
      const row = btn.closest("tr");
      if (confirm("Tem certeza que deseja remover este item?")) {
        row.remove();
      }
    }