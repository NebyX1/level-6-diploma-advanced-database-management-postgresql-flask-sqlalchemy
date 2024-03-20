from .db import db
from flask_login import UserMixin


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def check_password(self, password_attempt):
        return self.password == password_attempt

    def __repr__(self):
        return "<Admin %r>" % self.id

    def serialize(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Country(db.Model):
    __tablename__ = "country"
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Country {self.country_name}>"

    def serialize(self):
        return {"country_id": self.country_id, "country_name": self.country_name}


class Client(db.Model):
    __tablename__ = "client"
    client_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(255), nullable=False)
    country_id = db.Column(
        db.Integer, db.ForeignKey("country.country_id"), nullable=False
    )
    country = db.relationship("Country", backref=db.backref("clients", lazy=True))

    def __repr__(self):
        return f"<Client {self.client_name}>"

    def serialize(self):
        return {
            "client_id": self.client_id,
            "client_name": self.client_name,
            "country_id": self.country_id,
        }


class Game(db.Model):
    __tablename__ = "game"
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Game {self.game_name}>"

    def serialize(self):
        return {
            "game_id": self.game_id,
            "game_name": self.game_name,
            "genre": self.genre,
            "price": self.price,
        }


class Purchase(db.Model):
    __tablename__ = "purchase"
    purchase_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.client_id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.game_id"), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    client = db.relationship("Client", backref=db.backref("purchases", lazy=True))
    game = db.relationship("Game", backref=db.backref("purchases", lazy=True))

    def __repr__(self):
        return f"<Purchase {self.purchase_id}>"

    def serialize(self):
        return {
            "purchase_id": self.purchase_id,
            "client_id": self.client_id,
            "game_id": self.game_id,
            "purchase_date": self.purchase_date.isoformat(),
            "amount": self.amount,
        }
