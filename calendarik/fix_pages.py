# Исправляем forgot_password.html
with open('templates/auth/forgot_password.html', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('ведите ваш email', 'Введите ваш email')
content = content.replace('тправить', 'Отправить')
content = content.replace('ведите email', 'Введите email')
content = content.replace('ведите корректный email', 'Введите корректный email')
content = content.replace('оготип', 'Логотип')
with open('templates/auth/forgot_password.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('forgot_password.html - OK')