from database import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    date_meal = db.Column(db.DateTime, nullable=False)

    # Adiciona chave estrangeira
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)