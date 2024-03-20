from app import app
from database.db import db
from database.models import Country, Client, Game, Purchase  # noqa: F401

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=3500)
    # app.run()
