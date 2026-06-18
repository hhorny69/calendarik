with open("calendarik/app/routes/auth.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify({'message': 'Регистрация прошла успешно'}), 201"""

new = """    role = data.get('role', 'employee')
    if role not in ('employee', 'organizer'):
        role = 'employee'
    user = User(username=username, email=email, role='employee')
    if role == 'organizer':
        user.organizer_request = 'pending'
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify({'message': 'Регистрация прошла успешно'}), 201"""

content = content.replace(old, new)
with open("calendarik/app/routes/auth.py", "w", encoding="utf-8") as f:
    f.write(content)
print("OK")
