from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Reagente, Meio, Agendamento
import os

app = Flask(__name__)

# Configuração do banco de dados via variável de ambiente
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario == "admin" and senha == "senha123":
            return "Login aceito"
        else:
            return "Login inválido", 401

    reagentes = Reagente.query.all()
    meios = Meio.query.all()
    agenda = Agendamento.query.all()
    return render_template("index.html", reagentes=reagentes, meios=meios, agenda=agenda)

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
app.run(debug=True)
