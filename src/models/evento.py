from .user import db
from datetime import datetime

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data_evento = db.Column(db.DateTime, nullable=False)
    imagem_url = db.Column(db.String(255), nullable=True)
    link_saiba_mais = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Evento {self.titulo}>'

