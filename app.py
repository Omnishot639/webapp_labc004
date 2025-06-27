from flask import Flask, request, render_template

app = Flask(__name__)
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Reagente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    quantidade = db.Column(db.String(50))
    validade = db.Column(db.String(50))
    localizacao = db.Column(db.String(100))

class Meio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    quantidade = db.Column(db.String(50))
    validade = db.Column(db.String(50))
    localizacao = db.Column(db.String(100))

class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipamento = db.Column(db.String(100))
    usuario = db.Column(db.String(100))
    data = db.Column(db.String(50))
    horario = db.Column(db.String(50))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario == "admin" and senha == "senha123":
            return "Login aceito"
        else:
            return "Login inválido", 401
    return render_template("index.html")
