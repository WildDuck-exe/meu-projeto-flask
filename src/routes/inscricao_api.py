from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user # Import decorators
from src.models.user import db
from src.models.inscricao import Inscricao
from datetime import datetime

inscricao_bp = Blueprint("inscricao_bp", __name__)

# Rota para criar uma nova inscrição (Pública)
@inscricao_bp.route("/inscricoes", methods=["POST"])
def create_inscricao():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Nenhum dado recebido"}), 400

    # Validação básica (campos obrigatórios conforme documento)
    if not data.get("nome_completo") or not data.get("email") or not data.get("telefone") or data.get("concorda_termos") is None:
        return jsonify({"message": "Campos obrigatórios ausentes (Nome, Email, Telefone, Concorda Termos)"}), 400

    try:
        # Tentar converter data de nascimento se fornecida
        data_nascimento = None
        if data.get("data_nascimento"):
            try:
                # Ajustar o formato conforme o que o frontend enviará (ex: YYYY-MM-DD)
                data_nascimento = datetime.strptime(data["data_nascimento"], "%Y-%m-%d").date()
            except ValueError:
                # Permitir data nula se o formato for inválido, mas logar um aviso
                print(f"Aviso: Formato inválido para data de nascimento recebida: {data.get('data_nascimento')}")
                pass # data_nascimento continua None

        nova_inscricao = Inscricao(
            # Dados Pessoais
            nome_completo=data["nome_completo"],
            data_nascimento=data_nascimento,
            genero=data.get("genero"),
            cpf=data.get("cpf"),
            rg=data.get("rg"),
            # Contato
            email=data["email"],
            telefone=data["telefone"],
            endereco_cep=data.get("endereco_cep"),
            endereco_rua=data.get("endereco_rua"),
            endereco_bairro=data.get("endereco_bairro"),
            endereco_numero=data.get("endereco_numero"),
            endereco_complemento=data.get("endereco_complemento"),
            # Informações da Inscrição
            nome_evento_atividade=data.get("nome_evento_atividade"),
            area_interesse=data.get("area_interesse"),
            turno_preferencia=data.get("turno_preferencia"),
            necessidade_especial=data.get("necessidade_especial", False),
            descricao_necessidade=data.get("descricao_necessidade"),
            como_soube=data.get("como_soube"),
            # Consentimentos
            concorda_termos=bool(data["concorda_termos"]),
            autoriza_imagem=bool(data.get("autoriza_imagem", False)),
            # Newsletter
            assina_newsletter=bool(data.get("assina_newsletter", False))
        )

        db.session.add(nova_inscricao)
        db.session.commit()

        # Pode retornar o ID ou uma mensagem de sucesso
        return jsonify({"message": "Inscrição realizada com sucesso!", "id_inscricao": nova_inscricao.id}), 201

    except Exception as e:
        db.session.rollback()
        # Logar o erro real no servidor é importante
        print(f"Erro ao criar inscrição: {e}")
        return jsonify({"error": "Ocorreu um erro ao processar sua inscrição."}), 500

# --- Rotas para Administração (Protegidas) ---

# Rota para listar todas as inscrições (requer admin)
@inscricao_bp.route("/inscricoes", methods=["GET"])
@login_required
def get_inscricoes():
    if not current_user.is_admin:
        return jsonify({"message": "Acesso não autorizado"}), 403

    try:
        inscricoes = Inscricao.query.order_by(Inscricao.data_inscricao.desc()).all()
        inscricoes_list = [
            {
                "id": ins.id,
                "nome_completo": ins.nome_completo,
                "email": ins.email,
                "telefone": ins.telefone,
                "nome_evento_atividade": ins.nome_evento_atividade,
                "data_inscricao": ins.data_inscricao.isoformat(),
                # Adicionar mais campos conforme necessário para a listagem
            }
            for ins in inscricoes
        ]
        return jsonify(inscricoes_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter detalhes de uma inscrição (requer admin)
@inscricao_bp.route("/inscricoes/<int:id>", methods=["GET"])
@login_required
def get_inscricao(id):
    if not current_user.is_admin:
        return jsonify({"message": "Acesso não autorizado"}), 403

    try:
        inscricao = Inscricao.query.get(id)
        if not inscricao:
            return jsonify({"message": "Inscrição não encontrada"}), 404

        # Retornar todos os dados da inscrição
        inscricao_data = {}
        for key in Inscricao.__table__.columns.keys():
            value = getattr(inscricao, key)
            # Convert date/datetime objects to ISO format string
            if isinstance(value, (datetime, date)): # Import date from datetime
                inscricao_data[key] = value.isoformat()
            else:
                inscricao_data[key] = value

        return jsonify(inscricao_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para deletar uma inscrição (requer admin)
@inscricao_bp.route("/inscricoes/<int:id>", methods=["DELETE"])
@login_required
def delete_inscricao(id):
    if not current_user.is_admin:
        return jsonify({"message": "Acesso não autorizado"}), 403

    inscricao = Inscricao.query.get(id)
    if not inscricao:
        return jsonify({"message": "Inscrição não encontrada"}), 404

    try:
        db.session.delete(inscricao)
        db.session.commit()
        return jsonify({"message": "Inscrição deletada com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Import date
from datetime import date

