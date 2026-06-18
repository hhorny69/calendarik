with open('templates/auth/login.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'margin-top:16px; font-size:13px;' + chr(39) + '>Забыли пароль?',
    'margin-top:24px; font-size:13px;' + chr(39) + '>Забыли пароль?'
)

with open('templates/auth/login.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')