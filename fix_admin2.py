with open("calendarik/app/routes/admin.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "('/api/admin/organizer-requests/<int:user_id>/approve', methods=['POST'])",
    ""
)

fix = """
@admin_bp.route('/api/admin/organizer-requests', methods=['GET'])
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
"""

content = content.replace(
    "@login_required\ndef approve_organizer(user_id):",
    fix + "\n@admin_bp.route('/api/admin/organizer-requests/<int:user_id>/approve', methods=['POST'])\n@login_required\ndef approve_organizer(user_id):"
)

with open("calendarik/app/routes/admin.py", "w", encoding="utf-8") as f:
    f.write(content)
print("OK")
