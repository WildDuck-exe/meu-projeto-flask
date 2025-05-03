from .user import db
from datetime import datetime

class Inscricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Etapa 1: Dados Pessoais
    nome_completo = db.Column(db.String(150), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=True)
    genero = db.Column(db.String(50), nullable=True)
    cpf = db.Column(db.String(14), nullable=True, unique=True) # Formato XXX.XXX.XXX-XX
    rg = db.Column(db.String(20), nullable=True, unique=True)

    # Etapa 2: Contato
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco_cep = db.Column(db.String(9), nullable=True) # Formato XXXXX-XXX
    endereco_rua = db.Column(db.String(200), nullable=True)
    endereco_bairro = db.Column(db.String(100), nullable=True)
    endereco_numero = db.Column(db.String(20), nullable=True)
    endereco_complemento = db.Column(db.String(100), nullable=True) # Adicionado para complemento

    # Etapa 3: Informações da Inscrição
    nome_evento_atividade = db.Column(db.String(200), nullable=True)
    area_interesse = db.Column(db.String(100), nullable=True)
    turno_preferencia = db.Column(db.String(50), nullable=True)
    necessidade_especial = db.Column(db.Boolean, default=False)
    descricao_necessidade = db.Column(db.Text, nullable=True)
    como_soube = db.Column(db.String(100), nullable=True)

    # Etapa 4: Consentimentos
    concorda_termos = db.Column(db.Boolean, nullable=False, default=False)
    autoriza_imagem = db.Column(db.Boolean, default=False)

    # Etapa 5: Newsletter
    assina_newsletter = db.Column(db.Boolean, default=False)

    # Metadados
    data_inscricao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Inscricao {self.nome_completo} - {self.email}>'

