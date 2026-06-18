with open('templates/auth/login.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<strong>Сбросить пароль</strong>',
    'Сбросить пароль'
)
content = content.replace(
    'margin-top:8px; font-size:13px;' + chr(39) + '>Забыли пароль?',
    'margin-top:16px; font-size:13px;' + chr(39) + '>Забыли пароль?'
)

with open('templates/auth/login.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')