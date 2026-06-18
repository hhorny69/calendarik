with open('templates/auth/login.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<p style=' + chr(39) + 'margin-top:16px; font-size:13px;' + chr(39) + '><a href=' + chr(39) + '/forgot-password' + chr(39) + ' style=' + chr(39) + 'color:#8B1A2B; text-decoration:none;' + chr(39) + '>Забыли пароль?</a></p>',
    '<p style=' + chr(39) + 'margin-top:8px; font-size:13px;' + chr(39) + '>Забыли пароль? <a href=' + chr(39) + '/forgot-password' + chr(39) + ' class=' + chr(39) + 'link-dark' + chr(39) + '><strong>Сбросить пароль</strong></a></p>'
)

with open('templates/auth/login.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')