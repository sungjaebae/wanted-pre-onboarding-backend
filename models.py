from typing import Optional

from sqlmodel import Field, SQLModel, Relationship, String, Text


class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(String(25), nullable=False)
    password: str = Field(String(44), nullable=False)
    articles: list["Article"] = Relationship(
        back_populates='user')

    def __repr__(self):
        return f"<User email={self.email} password={self.password} articles={self.articles}>"


class Article(SQLModel, table=True):
    __tablename__ = 'articles'
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='users.id')
    title: str = Field(String(100), nullable=False)
    body: str = Field(Text, nullable=False)
    user: User = Relationship(back_populates='articles')

    def __repr__(self):
        return f"<Article title={self.title} body={self.body} by User.email={self.user.email}>"
