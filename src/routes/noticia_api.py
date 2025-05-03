from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user # Import decorators
from src.models.user import db
from src.models.noticia import Noticia
from datetime import datetime

noticia_bp = Blueprint("noticia_bp", __name__)

# Rota para obter todas as notícias (Pública)
@noticia_bp.route("/noticias", methods=["GET"])
def get_noticias():
    try:
        noticias = Noticia.query.order_by(Noticia.data_publicacao.desc()).all()
        noticias_list = [
            {
                "id": nt.id,
                "titulo": nt.titulo,
                "conteudo": nt.conteudo[:200] + "..." if nt.conteudo and len(nt.conteudo) > 200 else nt.conteudo, # Truncate content for list view
                "data_publicacao": nt.data_publicacao.isoformat() if nt.data_publicacao else None,
                "imagem_url": nt.imagem_url,
                "autor": nt.autor,
            }
            for nt in noticias
        ]
        return jsonify(noticias_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter uma notícia específica pelo ID (Pública)
@noticia_bp.route("/noticias/<int:id>", methods=["GET"])
def get_noticia(id):
    try:
        noticia = Noticia.query.get(id)
        if noticia:
            noticia_data = {
                "id": noticia.id,
                "titulo": noticia.titulo,
                "conteudo": noticia.conteudo,
                "data_publicacao": noticia.data_publicacao.isoformat() if noticia.data_publicacao else None,
                "imagem_url": noticia.imagem_url,
                "autor": noticia.autor,
            }
            return jsonify(noticia_data), 200
        else:
            return jsonify({"message": "Notícia não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Rotas para Administração (Protegidas) ---

# Rota para criar uma nova notícia (POST - Admin)
@noticia_bp.route("/noticias", methods=["POST"])
@login_required
def create_noticia():
    if not current_user.is_admin:
        return jsonify({"message": "Acesso não autorizado"}), 403

    data = request.get_json()
    if not data or not data.get("titulo") or not data.get("conteudo"):
        return jsonify({"message": "Dados incompletos (título e conteúdo são obrigatórios)"}), 400

    try:
        nova_noticia = Noticia(
            titulo=data["titulo"],
            conteudo=data["conteudo"],
            imagem_url=data.get("imagem_url"),
            autor=data.get("autor", current_user.username) # Default to logged-in admin username
            # data_publicacao é definida por default=datetime.utcnow no modelo
        )
        db.session.add(nova_noticia)
        db.session.commit()
        return jsonify({"message": "Notícia criada com sucesso", "id": nova_noticia.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Rota para atualizar uma notícia (PUT - Admin)
@noticia_bp.route("/noticias/<int:id>", methods=["PUT"])
@login_required
def update_noticia(id):
    if not current_user.is_admin:
        return jsonify({"message": "Acesso não autorizado"}), 403

    noticia = Noticia.query.get(id)
    if not noticia:
        return jsonify({"message": "Notícia não encontrada"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "Nenhum dado fornecido para atualização"}), 400

    try:
        if "titulo" in data: noticia.titulo = data["titulo"]
        if "conteudo" in data: noticia.conteudo = data["conteudo"]
        if "imagem_url" in data: noticia.imagem_url = data["imagem_url"]
        if "autor" in data: noticia.autor = data["autor"]

        db.session.commit()
        return jsonify({"message": "Notícia atualizada com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Rota para deletar uma notícia (DELETE - Admin)
@noticia_bp.route("/noticias/<int:id>", methods=["DELETE"])
@login_required
def delete_noticia(id):
    if not current_user.is_admin:
        return jsonify({"message": "Acesso não autorizado"}), 403

    noticia = Noticia.query.get(id)
    if not noticia:
        return jsonify({"message": "Notícia não encontrada"}), 404

    try:
        db.session.delete(noticia)
        db.session.commit()
        return jsonify({"message": "Notícia deletada com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

