from flask import Flask, request, jsonify
from models.user import User
from models.meal import Meal
from database import db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet-api'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            return jsonify({"message": "Autenticação realizada com sucesso!"})
        
    return jsonify({"message": "Credenciais inválidas!"}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout efetuado com sucesso!"})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso!"})
    
    return jsonify({"message": "Dados inválidos!"}), 400

@app.route('/user/<int:user_id>', methods=['GET'])
@login_required
def read_user(user_id):
    user = User.query.get(user_id)

    if user:
        return jsonify({"username": user.username})
    
    return jsonify({"message": "Usuário não encontrado!"}), 404

@app.route('/user', methods=['PUT'])
@login_required
def update_user():
    user = current_user
    data = request.json
    new_password = data.get('password')

    if new_password:
        hashed_new_password = bcrypt.hashpw(str.encode(new_password), bcrypt.gensalt())
        user.password = hashed_new_password
        db.session.commit()
        return jsonify({"message": f"Usuário {current_user.id} atualizado com sucesso!"})
    
    return jsonify({"message": "Dados inválidos"}), 400

@app.route('/user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if current_user.role != 'admin':
        return jsonify({"message": "Operação não permitida!"}), 403

    if user_id == current_user.id:
        return jsonify({"message": "Não foi permitido deletar!"}), 403
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {user_id} deletado com sucesso!"})
    
    return jsonify({"message": "Usuário não encontrado!"}), 404

@app.route('/meal', methods=['POST'])
@login_required
def create_meal():
    data = request.json
    meal_name = data.get('name')
    meal_description = data.get('description')
    date_meal = data.get('date_meal')
    on_diet = data.get('on_diet')

    if meal_name and meal_description and date_meal:
        meal = Meal(name=meal_name, description=meal_description, date_meal=date_meal, user_id=current_user.id, on_diet=on_diet)
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Refeição adicionada com sucesso!"})
    
    return jsonify({"message": "Dados inválidos!"}), 400

@app.route('/meal', methods=['GET'])
@login_required
def read_meals():
    meals = Meal.query.filter_by(user_id=current_user.id).all()

    return [
        {
            "id": meal.id,
            "name": meal.name,
            "description": meal.description,
            "date": meal.date_meal,
            "on_diet": meal.on_diet
        }
        for meal in meals
    ]

@app.route('/meal/<int:meal_id>', methods=['GET'])
@login_required
def read_meal(meal_id):
    meal = Meal.query.filter_by(user_id=current_user.id, id=meal_id).first()

    if meal:
        return {
            "id": meal.id,
            "name": meal.name,
            "description": meal.description,
            "date": meal.date_meal,
            "on_diet": meal.on_diet
        }
    
    return jsonify({"message": "Refeição não encontrada!"}), 404

@app.route('/meal/<int:meal_id>', methods=['PUT'])
@login_required
def update_meal(meal_id):
    data = request.json
    new_name = data.get('name')
    new_description = data.get('description')
    new_date = data.get('date_meal')
    new_on_diet = data.get('on_diet')
    meal = Meal.query.filter_by(user_id=current_user.id, id=meal_id).first()

    if not meal:
        return jsonify({"message": "Refeição não encontrada!"}), 404

    if new_name and new_description and new_date:
        meal.name = new_name
        meal.description = new_description
        meal.date_meal = new_date
        meal.on_diet = new_on_diet
        db.session.commit()
        
        return jsonify({"message": "Refeição atualizada com sucesso!"})
    
    return jsonify({"message": "Dados inválidos!"}), 400

@app.route('/meal/<int:meal_id>', methods=['DELETE'])
@login_required
def delete_meal(meal_id):
    meal = Meal.query.filter_by(user_id=current_user.id, id=meal_id).first()

    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": "Refeição deletada com sucesso!"})
    
    return jsonify({"message": "Refeição não encontrada!"}), 404

if __name__ == "__main__":
    app.run(debug=True)