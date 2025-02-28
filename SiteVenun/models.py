from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

## Usuário

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    senha = db.Column(db.String(100), nullable=False)

## Produto

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    imagem_one = db.Column(db.String(200), nullable=True)
    imagem_two = db.Column(db.String(200), nullable=True)
