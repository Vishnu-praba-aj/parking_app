from flask import Blueprint, request, jsonify, render_template_string
from models.user import User
from models import db

auth_bp = Blueprint('auth', __name__)

# Optional: serve a simple HTML form for GET
@auth_bp.route('/login', methods=['GET'])
def login_form():
    return render_template_string("""
    <form method="POST" action="/login">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <button type="submit">Login</button>
    </form>
    """)


@auth_bp.route('/register', methods=['GET'])
def register_form():
    return render_template_string("""
    <form method="POST" action="/register">
        Username: <input name="username"><br>
        Email: <input name="email" type="email" required><br>
        Password: <input name="password" type="password"><br>
        <button type="submit">Register</button>
    </form>
    """)


# Existing POST routes

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.form if request.form else request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Username, email and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.form if request.form else request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': f'Welcome, {user.username}!'}), 200
