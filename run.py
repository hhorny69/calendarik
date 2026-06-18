import os
from app import create_app, db
from app.models import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Создаём админа если его нет
        admin = User.query.filter_by(username='admin').first()
        if admin:
            admin.role = 'admin'
            db.session.commit()
            print('Роль admin обновлена!')
        else:
            print('Пользователь admin не найден')
    
    app.run(host='0.0.0.0', port=5000, debug=False)