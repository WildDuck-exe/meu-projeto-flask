from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user # Import decorators
from src.models.user import db
from src.models.evento import Evento
from datetime import datetime

evento_bp = Blueprint("evento_bp", __name__)

# Rota para obter todos os eventos (Pública)
@evento_bp.route("/eventos", methods=["GET"])
def get_eventos():
    try:
        eventos = Evento.query.order_by(Evento.data_evento.desc()).all()
        eventos_list = [
            {
                "id": ev.id,
                "titulo": ev.titulo,
                "descricao": ev.descricao,
                "data_evento": ev.data_evento.isoformat() if ev.data_evento else None,
                "imagem_url": ev.imagem_url,
                "link_saiba_mais": ev.link_saiba_mais,
                "criado_em": ev.criado_em.isoformat() if ev.criado_em else None,
            }
            for ev in eventos
        ]
        return jsonify(eventos_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter um evento específico pelo ID (Pública)
@evento_bp.route("/eventos/<int:id>", methods=["GET"])
def get_evento(id):
    try:
        evento = Evento.query.get(id)
        if evento:
            evento_data = {
                "id": evento.id,
                "titulo": evento.titulo,
                "descricao": evento.descricao,
                "data_evento": evento.data_evento.isoformat() if evento.data_evento else None,
                "imagem_url": evento.imagem_url,
                "link_saiba_mais": evento.link_saiba_mais,
                "criado_em": evento.criado_em.isoformat() if evento.criado_em else None,
            }
            return jsonify(evento_data), 200
        else:
            return jsonify({"message": "Evento não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Rotas para Administração (Protegidas) ---

# Rota para criar um novo evento (POST - Admin)
@evento_bp.route("/eventos", methods=["POST"])
@login_required
def create_evento():
    if not current_user.is_admin:
        return jsonify({"message": "Acesso não autorizado"}), 403

    data = request.get_json()
    if not data or not data.get("titulo") or not data.get("data_evento"):
        return jsonify({"message": "Dados incompletos"}), 400

    try:
        # Validar e converter data
        data_evento_dt = None
        if data.get("data_evento"):
             try:
                 data_evento_dt = datetime.fromisoformat(data["data_evento"].replace("Z", "+00:00")) # Handle ISO format
             except ValueError:
                 return jsonify({"message": "Formato inválido para data_evento (use ISO 8601)"}), 400
        else:
             return jsonify({"message": "data_evento é obrigatório"}), 400

        novo_evento = Evento(
            titulo=data["titulo"],
            descricao=data.get("descricao"),
            data_evento=data_evento_dt,
            imagem_url=data.get("imagem_url"),
            link_saiba_mais=data.get("link_saiba_mais")
        )
        db.session.add(novo_evento)
        db.session.commit()
        return jsonify({"message": "Evento criado com sucesso", "id": novo_evento.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Rota para atualizar um evento (PUT - Admin)
@evento_bp.route("/eventos/<int:id>", methods=["PUT"])
@login_required
def update_evento(id):
    if not current_user.is_admin:
        return jsonify({"message": "Acesso não autorizado"}), 403

    evento = Evento.query.get(id)
    if not evento:
        return jsonify({"message": "Evento não encontrado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "Nenhum dado fornecido para atualização"}), 400

    try:
        if "titulo" in data: evento.titulo = data["titulo"]
        if "descricao" in data: evento.descricao = data["descricao"]
        if "data_evento" in data:
            try:
                evento.data_evento = datetime.fromisoformat(data["data_evento"].replace("Z", "+00:00"))
            except ValueError:
                 return jsonify({"message": "Formato inválido para data_evento (use ISO 8601)"}), 400
        if "imagem_url" in data: evento.imagem_url = data["imagem_url"]
        if "link_saiba_mais" in data: evento.link_saiba_mais = data["link_saiba_mais"]

        db.session.commit()
        return jsonify({"message": "Evento atualizado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Rota para deletar um evento (DELETE - Admin)
@evento_bp.route("/eventos/<int:id>", methods=["DELETE"])
@login_required
def delete_evento(id):
    if not current_user.is_admin:
        return jsonify({"message": "Acesso não autorizado"}), 403

    evento = Evento.query.get(id)
    if not evento:
        return jsonify({"message": "Evento não encontrado"}), 404

    try:
        db.session.delete(evento)
        db.session.commit()
        return jsonify({"message": "Evento deletado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

