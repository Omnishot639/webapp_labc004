from app import db

class Reagente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.String(50))
    validade = db.Column(db.String(20))
    localizacao = db.Column(db.String(100))

class Meio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.String(50))
    validade = db.Column(db.String(20))
    localizacao = db.Column(db.String(100))

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipamento = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(100))
    data = db.Column(db.String(20))
    horario = db.Column(db.String(20))
