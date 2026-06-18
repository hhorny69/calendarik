from flask import Blueprint, send_from_directory, jsonify, request
from flask_login import current_user, login_required
from app.models import User, Event, EventParticipant
from app import db
import os

calendar_bp = Blueprint('calendar', __name__)
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '../../templates')

@calendar_bp.route('/index')
def index():
    return send_from_directory(os.path.abspath(TEMPLATES_DIR), 'index.html')

@calendar_bp.route('/profile')
def profile():
    return send_from_directory(os.path.abspath(TEMPLATES_DIR), 'profile.html')

@calendar_bp.route('/apply')
def apply():
    return send_from_directory(os.path.abspath(TEMPLATES_DIR), 'apply.html')

@calendar_bp.route('/organizer')
def organizer():
    return send_from_directory(os.path.abspath(TEMPLATES_DIR), 'organizer.html')

@calendar_bp.route('/api/profile')
def api_profile():
    if current_user.is_authenticated:
        roles = {
            'admin': 'Администратор',
            'organizer': 'Организатор',
            'employee': 'Сотрудник'
        }
        return jsonify({
            'username': current_user.username,
            'email': current_user.email,
            'role': roles.get(current_user.role, 'Сотрудник'),
            'role_code': current_user.role,
            'full_name': current_user.full_name or '',
            'department': current_user.department or '',
            'position': current_user.position or '',
            'phone': current_user.phone or ''
        })
    return jsonify({'error': 'Не авторизован'}), 401

@calendar_bp.route('/api/profile', methods=['POST'])
@login_required
def update_profile():
    data = request.get_json()
    current_user.full_name = data.get('full_name', current_user.full_name)
    current_user.department = data.get('department', current_user.department)
    current_user.position = data.get('position', current_user.position)
    current_user.phone = data.get('phone', current_user.phone)
    db.session.commit()
    return jsonify({'message': 'Профиль обновлен'}), 200

@calendar_bp.route('/api/stats')
@login_required
def get_stats():
    if current_user.role not in ['admin', 'organizer']:
        return jsonify({'error': 'Нет доступа'}), 403
    total_events = Event.query.filter_by(status='approved').count()
    my_registrations = EventParticipant.query.filter_by(user_id=current_user.id).count()
    pending_events = Event.query.filter_by(status='pending').count()
    total_users = User.query.count()
    return jsonify({
        'total_events': total_events,
        'my_registrations': my_registrations,
        'pending_events': pending_events,
        'total_users': total_users
    })

@calendar_bp.route('/api/my-registrations')
@login_required
def my_registrations():
    regs = EventParticipant.query.filter_by(user_id=current_user.id).all()
    result = []
    for r in regs:
        event = Event.query.get(r.event_id)
        if event:
            result.append({
                'event_id': event.id,
                'title': event.title,
                'location': event.location or '',
                'event_type': event.event_type or '',
                'start': event.start_time.isoformat(),
                'status': r.status,
                'registration_date': r.registration_date.strftime('%d.%m.%Y')
            })
    return jsonify(result)