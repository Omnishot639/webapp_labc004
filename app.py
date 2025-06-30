from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Reagente, Meio, Agendamento, Usuario
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY", "chave-fallback-insegura")

db.init_app(app)

@app.before_request
def proteger_rotas():
    rotas_livres = ['index', 'login', 'static']
    if request.endpoint not in rotas_livres and "usuario_id" not in session:
        return redirect(url_for("login"))

@app.route("/", methods=["GET"])
def index():
    reagentes = Reagente.query.all()
    meios = Meio.query.all()
    agenda = Agendamento.query.all()
    usuario = Usuario.query.get(session.get("usuario_id"))
    return render_template("index.html", reagentes=reagentes, meios=meios, agenda=agenda, usuario=usuario)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form.get("usuario")
        senha = request.form.get("senha")
        user = Usuario.query.filter_by(nome=nome).first()
        if user and check_password_hash(user.senha, senha):
            session["usuario_id"] = user.id
            return redirect(url_for("index"))
        else:
            return "Login inválido", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    if not is_admin(): return "Acesso negado", 403
    usuarios = Usuario.query.all()
    return jsonify([{"id": u.id, "nome": u.nome, "is_admin": u.is_admin} for u in usuarios])

@app.route("/usuarios", methods=["POST"])
def criar_usuario():
    if not is_admin(): return "Acesso negado", 403
    data = request.json
    senha_hash = generate_password_hash(data["senha"])
    novo = Usuario(nome=data["nome"], senha=senha_hash, is_admin=data.get("is_admin", False))
    db.session.add(novo)
    db.session.commit()
    return jsonify({"message": "Usuário criado"}), 201

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def remover_usuario(id):
    if not is_admin(): return "Acesso negado", 403
    if session["usuario_id"] == id:
        return jsonify({"message": "Você não pode se remover"}), 403
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuário removido"})

def is_admin():
    uid = session.get("usuario_id")
    if not uid:
        return False
    user = Usuario.query.get(uid)
    return user and user.is_admin

@app.route("/api/reagentes", methods=["GET"])
def listar_reagentes():
    reagentes = Reagente.query.all()
    return jsonify([{
        "id": r.id,
        "nome": r.nome,
        "quantidade": r.quantidade,
        "validade": r.validade,
        "localizacao": r.localizacao
    } for r in reagentes])

@app.route("/api/meios", methods=["GET"])
def listar_meios():
    meios = Meio.query.all()
    return jsonify([{
        "id": m.id,
        "nome": m.nome,
        "quantidade": m.quantidade,
        "validade": m.validade,
        "localizacao": m.localizacao
    } for m in meios])

@app.route("/api/agenda", methods=["GET"])
def listar_agenda():
    agenda = Agendamento.query.all()
    return jsonify([{
        "id": a.id,
        "equipamento": a.equipamento,
        "usuario": a.usuario,
        "data": a.data,
        "horario": a.horario
    } for a in agenda])

@app.route("/api/reagentes", methods=["POST"])
def adicionar_reagente():
    data = request.json
    novo = Reagente(
        nome=data["nome"],
        quantidade=data["quantidade"],
        validade=data["validade"],
        localizacao=data["localizacao"]
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"message": "Reagente adicionado", "id": novo.id}), 201


@app.route("/api/reagentes/<int:id>", methods=["PUT"])
def editar_reagente(id):
    reagente = Reagente.query.get_or_404(id)
    data = request.json
    reagente.nome = data["nome"]
    reagente.quantidade = data["quantidade"]
    reagente.validade = data["validade"]
    reagente.localizacao = data["localizacao"]
    db.session.commit()
    return jsonify({"message": "Reagente atualizado"})


@app.route("/api/reagentes/<int:id>", methods=["DELETE"])
def deletar_reagente(id):
    reagente = Reagente.query.get_or_404(id)
    db.session.delete(reagente)
    db.session.commit()
    return jsonify({"message": "Reagente removido"})

@app.route("/api/meios", methods=["POST"])
def adicionar_meio():
    data = request.json
    novo = Meio(
        nome=data["nome"],
        quantidade=data["quantidade"],
        validade=data["validade"],
        localizacao=data["localizacao"]
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"message": "Meio adicionado", "id": novo.id}), 201


@app.route("/api/meios/<int:id>", methods=["PUT"])
def editar_meio(id):
    meio = Meio.query.get_or_404(id)
    data = request.json
    meio.nome = data["nome"]
    meio.quantidade = data["quantidade"]
    meio.validade = data["validade"]
    meio.localizacao = data["localizacao"]
    db.session.commit()
    return jsonify({"message": "Meio atualizado"})


@app.route("/api/meios/<int:id>", methods=["DELETE"])
def deletar_meio(id):
    meio = Meio.query.get_or_404(id)
    db.session.delete(meio)
    db.session.commit()
    return jsonify({"message": "Meio removido"})

@app.route("/api/agenda", methods=["POST"])
def adicionar_agendamento():
    data = request.json
    novo = Agendamento(
        equipamento=data["equipamento"],
        usuario=data["usuario"],
        data=data["data"],
        horario=data["horario"]
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"message": "Agendamento adicionado", "id": novo.id}), 201


@app.route("/api/agenda/<int:id>", methods=["PUT"])
def editar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    data = request.json
    agendamento.equipamento = data["equipamento"]
    agendamento.usuario = data["usuario"]
    agendamento.data = data["data"]
    agendamento.horario = data["horario"]
    db.session.commit()
    return jsonify({"message": "Agendamento atualizado"})


@app.route("/api/agenda/<int:id>", methods=["DELETE"])
def deletar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    db.session.delete(agendamento)
    db.session.commit()
    return jsonify({"message": "Agendamento removido"})

with app.app_context():
    db.create_all()
    if not Usuario.query.filter_by(nome="admin").first():
        senha_admin = os.getenv("ADMIN_PASSWORD", "senha123")
        senha_hash = generate_password_hash(senha_admin)
        admin = Usuario(nome="admin", senha=senha_hash, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado com sucesso.")

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)