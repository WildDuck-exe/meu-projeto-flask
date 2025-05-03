from .user import db
from datetime import datetime

class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_publicacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    imagem_url = db.Column(db.String(255), nullable=True)
    autor = db.Column(db.String(100), nullable=True) # Ou chave estrangeira para usuário

    def __repr__(self):
        return f'<Noticia {self.titulo}>'

