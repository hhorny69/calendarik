with open('templates/auth/login.html', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("class='login-form'>", "class='login-form' style='padding: 40px;'>")
content = content.replace("href='/forgot-password' class='link-dark'>Забыли пароль?", "href='/forgot-password' style='color:#8B1A2B; text-decoration:none;'>Забыли пароль?")
with open('templates/auth/login.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')