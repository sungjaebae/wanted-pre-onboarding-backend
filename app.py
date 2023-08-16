from hashlib import sha256
from base64 import b64encode
from flask import Flask, request, jsonify
from connect import session
from models import User, Article
from auth_middleware import token_required, owner_of_article
from sqlmodel import select
import jwt
import os
app = Flask(__name__)
SECRET_KEY = os.environ.get('SECRET_KEY') or '12341234'
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email: str = data['email']
    password: str = data['password']
    # 유효성 검증
    if not email or email.find("@") == -1:
        return jsonify({"result": "fail", "message": "이메일 형식이 올바르지 않습니다."}), 404
    if session.exec(select(User).where(User.email == email).limit(1)).first():
        return jsonify({"result": "fail", "message": "이미 회원가입한 이메일입니다."}), 404
    if not password or len(password) < 8:
        return jsonify({"result": "fail", "message": "비밀번호는 8자 이상이어야 합니다."}), 404

    hashedPassword = b64encode(sha256(password.encode('utf-8')).digest())
    user = User(email=email, password=hashedPassword)
    session.add(user)
    session.commit()
    return jsonify({'result': 'success', "message": "회원가입 성공"})


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email: str = data['email']
    password: str = data['password']
    hashedPassword = b64encode(
        sha256(password.encode('utf-8')).digest()).decode('utf-8')
    user = session.exec(select(User).where(
        User.email == email).limit(1)).first()
    if not user:
        return jsonify({"result": "fail", "message": "존재하지 않는 이메일입니다."}), 404
    if user.password != hashedPassword:
        return jsonify({"result": "fail", "message": "비밀번호가 일치하지 않습니다."}), 404

    token = jwt.encode(
        {"email": email}, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({"result": "success", "message": "로그인 성공", "token": token})


@app.route('/api/article', methods=['POST'])
@token_required
def create_article(current_user: User):
    data = request.json
    title: str = data['title']
    body: str = data['body']
    article = Article(title=title, body=body, user=current_user)
    session.add(article)
    session.commit()
    return jsonify({"result": "success", "message": "게시글 작성 성공"})


@app.route('/api/article', methods=['GET'])
def get_articles():
    page = int(request.args["page"]) if "page" in request.args else 1
    articles = session.exec(
        select(Article).offset((page-1)*10).limit(10)).all()
    articles = list(map(lambda article: article.dict(), articles))
    return jsonify({"result": "success", "message": "게시글 목록 조회 성공", "articles": articles})


@app.route('/api/article/<article_id>', methods=['GET'])
def get_article_detail(article_id: int):
    article = session.exec(select(Article).where(
        Article.id == article_id)).first()
    article = article.dict()
    return jsonify({"result": "success", "message": "게시글 세부 조회 성공", "article": article})


@app.route('/api/article/<article_id>', methods=['PUT'])
@token_required
@owner_of_article
def put_article_detail(current_user: User, article_id: int):
    article = session.exec(select(Article).where(
        Article.id == article_id)).first()
    article.body = request.json["body"] if "body" in request.json else article.body
    article.title = request.json["title"] if "title" in request.json else article.title

    session.commit()
    return jsonify({"result": "success", "message": "게시글 수정 성공"})


@app.route('/api/article/<article_id>', methods=['DELETE'])
@token_required
@owner_of_article
def delete_article_detail(current_user: User, article_id: int):
    article = session.exec(select(Article).where(
        Article.id == article_id)).first()
    session.delete(article)
    session.commit()
    return jsonify({"result": "success", "message": "게시글 삭제 성공"})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
