from functools import wraps
import jwt
from flask import request
from connect import session
from flask import current_app
from models import User, Article
from sqlmodel import select


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "result": "fail",
                "message": "인증 토큰이 없습니다",
            }, 401
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = session.exec(select(User).where(
                User.email == data["email"]).limit(1)).first()
            if current_user is None:
                return {
                    "result": "fail",
                    "message": "인증 토큰이 유효하지 않습니다",
                }, 401

        except Exception as e:
            return {
                "result": "fail",
                "message": f"다음 오류가 발생했습니다: {str(e)}",
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated


def owner_of_article(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user: User = args[0]
        article_id = int(kwargs["article_id"])
        article = session.exec(select(Article).where(
            Article.id == article_id).where(Article.user_id == current_user.id).limit(1)).first()
        if article is None:
            return {
                "result": "fail",
                "message": "게시글이 존재하지 않거나 권한이 없습니다",
            }, 401

        return f(*args, **kwargs)

    return decorated
