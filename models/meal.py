from database import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    on_diet = db.Column(db.Boolean, nullable=False, default=True)
    date_meal = db.Column(db.DateTime, nullable=False)

    # Adiciona chave estrangeira
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)