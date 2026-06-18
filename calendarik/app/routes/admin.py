from flask import Blueprint, request, jsonify, send_from_directory
from flask_login import login_required, current_user
from app.models import User, Event, EventParticipant
from app import db
import os

admin_bp = Blueprint('admin', __name__)
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '../../templates')

@admin_bp.route('/admin')
def admin():
    return send_from_directory(os.path.abspath(TEMPLATES_DIR), 'admin.html')

@admin_bp.route('/api/admin/users')
@login_required
def get_users():
    if not current_user.is_admin():
        return jsonify({'error': 'Нет доступа'}), 403
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'role': u.role,
        'created_at': u.created_at.strftime('%d.%m.%Y')
    } for u in users])

@admin_bp.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Нет доступа'}), 403
    if user_id == current_user.id:
        return jsonify({'error': 'Нельзя удалить себя'}), 400
    user = User.query.get_or_404(user_id)
    EventParticipant.query.filter_by(user_id=user_id).delete()
    events = Event.query.filter_by(user_id=user_id).all()
    for event in events:
        EventParticipant.query.filter_by(event_id=event.id).delete()
        db.session.delete(event)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Пользователь удален'}), 200

@admin_bp.route('/api/admin/events')
@login_required
def get_all_events():
    if current_user.role not in ['admin', 'organizer']:
        return jsonify({'error': 'Нет доступа'}), 403
    if current_user.is_admin():
        events = Event.query.all()
    else:
        events = Event.query.filter_by(user_id=current_user.id).all()
    return jsonify([e.to_dict() for e in events])

@admin_bp.route('/api/admin/events/pending')
@login_required
def get_pending_events():
    if current_user.role not in ['admin', 'organizer']:
        return jsonify({'error': 'Нет доступа'}), 403
    if current_user.is_admin():
        events = Event.query.filter_by(status='pending').all()
    else:
        events = Event.query.filter_by(user_id=current_user.id, status='pending').all()
    return jsonify([e.to_dict() for e in events])

@admin_bp.route('/api/admin/events/<int:event_id>/approve', methods=['POST'])
@login_required
def approve_event(event_id):
    if current_user.role not in ['admin', 'organizer']:
        return jsonify({'error': 'Нет доступа'}), 403
    event = Event.query.get_or_404(event_id)
    event.status = 'approved'
    db.session.commit()
    return jsonify({'message': 'Мероприятие одобрено'}), 200

@admin_bp.route('/api/admin/events/<int:event_id>/reject', methods=['POST'])
@login_required
def reject_event(event_id):
    if current_user.role not in ['admin', 'organizer']:
        return jsonify({'error': 'Нет доступа'}), 403
    event = Event.query.get_or_404(event_id)
    event.status = 'rejected'
    db.session.commit()
    return jsonify({'message': 'Мероприятие отклонено'}), 200

@admin_bp.route('/api/admin/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Нет доступа'}), 403
    event = Event.query.get_or_404(event_id)
    EventParticipant.query.filter_by(event_id=event_id).delete()
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Мероприятие удалено'}), 200

@admin_bp.route('/api/admin/events/<int:event_id>', methods=['PUT'])
@login_required
def edit_event(event_id):
    if current_user.role not in ['admin', 'organizer']:
        return jsonify({'error': 'Нет доступа'}), 403
    event = Event.query.get_or_404(event_id)
    if current_user.role == 'organizer' and event.user_id != current_user.id:
        return jsonify({'error': 'Можно редактировать только свои мероприятия'}), 403
    data = request.get_json()
    if data.get('title'): event.title = data['title']
    if data.get('description'): event.description = data['description']
    if data.get('location'): event.location = data['location']
    db.session.commit()
    return jsonify({'message': 'Мероприятие обновлено'}), 200

@admin_bp.route('/api/admin/participants/<int:event_id>')
@login_required
def get_participants(event_id):
    if current_user.role not in ['admin', 'organizer']:
        return jsonify({'error': 'Нет доступа'}), 403
    participants = EventParticipant.query.filter_by(event_id=event_id).all()
    result = []
    for p in participants:
        user = User.query.get(p.user_id)
        if user:
            result.append({'user_id': p.user_id, 'username': user.username, 'email': user.email, 'status': p.status})
    return jsonify(result)
@admin_bp.route('/api/admin/organizer-requests')
@login_required
def get_organizer_requests():
    if not current_user.is_admin():
        return jsonify({'error': 'Нет доступа'}), 403
    users = User.query.filter_by(organizer_request='pending').all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'created_at': u.created_at.strftime('%d.%m.%Y')
    } for u in users])

@admin_bp.route


@admin_bp.route('/api/admin/organizer-requests/<int:user_id>/approve', methods=['POST'])
@login_required
def approve_organizer(user_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Нет доступа'}), 403
    user = User.query.get_or_404(user_id)
    user.role = 'organizer'
    user.organizer_request = 'approved'
    db.session.commit()
    return jsonify({'message': 'Роль организатора выдана'}), 200

@admin_bp.route('/api/admin/organizer-requests/<int:user_id>/reject', methods=['POST'])
@login_required
def reject_organizer(user_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Нет доступа'}), 403
    user = User.query.get_or_404(user_id)
    user.organizer_request = 'rejected'
    db.session.commit()
    return jsonify({'message': 'Заявка отклонена'}), 200
