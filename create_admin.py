import sys
sys.path.insert(0, 'calendarik')
from app import create_app, db
from app.models import User
app = create_app()
ctx = app.app_context()
ctx.push()
admin = User(username='admin', email='admin@admin.com', role='admin')
admin.set_password('admin123')
db.session.add(admin)
db.session.commit()
print('Админ создан: логин=admin пароль=admin123')
