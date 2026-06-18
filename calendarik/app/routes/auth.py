from flask import Blueprint, request, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db
import os

auth_bp = Blueprint('auth', __name__)

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '../../templates')

@auth_bp.route('/')
@auth_bp.route('/login')
def login():
    return send_from_directory(TEMPLATES_DIR + '/auth', 'login.html')

@auth_bp.route('/register')
def register():
    return send_from_directory(TEMPLATES_DIR + '/auth', 'register.html')

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Неверный логин или пароль'}), 401

    login_user(user)
    return jsonify({'message': 'Успешный вход', 'user_id': user.id}), 200

@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Пользователь уже существует'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email уже используется'}), 400

    role = data.get('role', 'employee')
    if role not in ('employee', 'organizer'):
        role = 'employee'
    user = User(username=username, email=email, role='employee')
    if role == 'organizer':
        user.organizer_request = 'pending'
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify({'message': 'Регистрация прошла успешно'}), 201

@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({'message': 'Выход выполнен'}), 200

@auth_bp.route('/forgot-password')
def forgot_password():
    import os
    from flask import send_from_directory
    TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '../../templates/auth')
    return send_from_directory(os.path.abspath(TEMPLATES_DIR), 'forgot_password.html')