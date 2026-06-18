from flask import Blueprint, request, jsonify, send_from_directory
from flask_login import login_required, current_user
from app.models import Event, EventParticipant
from app import db
from datetime import datetime
import os

events_bp = Blueprint('events', __name__)
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '../../templates')

@events_bp.route('/events')
def events():
    return send_from_directory(os.path.abspath(TEMPLATES_DIR + '/events'), 'index.html')

@events_bp.route('/api/events', methods=['GET'])
@login_required
def get_events():
    events = Event.query.filter_by(status='approved').all()
    result = []
    for e in events:
        d = e.to_dict()
        d['participants_count'] = EventParticipant.query.filter_by(event_id=e.id).count()
        result.append(d)
    return jsonify(result)

@events_bp.route('/api/events', methods=['POST'])
@login_required
def create_event():
    data = request.get_json()
    event = Event(
        user_id=current_user.id,
        title=data.get('title'),
        description=data.get('description'),
        location=data.get('location', ''),
        event_type=data.get('event_type', 'other'),
        max_participants=data.get('max_participants'),
        start_time=datetime.fromisoformat(data.get('start_time')),
        end_time=datetime.fromisoformat(data.get('end_time')),
        color=data.get('color', '#3498db'),
        is_public=data.get('is_public', False),
        status='pending'
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201

@events_bp.route('/api/events/<int:event_id>/register', methods=['POST'])
@login_required
def register_for_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.status != 'approved':
        return jsonify({'error': 'Мероприятие недоступно'}), 400
    existing = EventParticipant.query.filter_by(event_id=event_id, user_id=current_user.id).first()
    if existing:
        return jsonify({'error': 'Вы уже записаны на это мероприятие'}), 400
    if event.max_participants:
        count = EventParticipant.query.filter_by(event_id=event_id).count()
        if count >= event.max_participants:
            return jsonify({'error': 'Мест больше нет'}), 400
    participant = EventParticipant(
        event_id=event_id,
        user_id=current_user.id,
        status='pending'
    )
    db.session.add(participant)
    db.session.commit()
    return jsonify({'message': 'Вы успешно записались!'}), 201

@events_bp.route('/api/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id and not current_user.is_admin():
        return jsonify({'error': 'Нет доступа'}), 403
    EventParticipant.query.filter_by(event_id=event_id).delete()
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Удалено'}), 200