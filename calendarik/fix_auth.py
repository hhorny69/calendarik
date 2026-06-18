with open('app/routes/auth.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'forgot-password' not in content:
    addon = chr(10) + chr(10) + '@auth_bp.route(' + chr(39) + '/forgot-password' + chr(39) + ')' + chr(10) + 'def forgot_password():' + chr(10) + '    import os' + chr(10) + '    from flask import send_from_directory' + chr(10) + '    TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), ' + chr(39) + '../../templates/auth' + chr(39) + ')' + chr(10) + '    return send_from_directory(os.path.abspath(TEMPLATES_DIR), ' + chr(39) + 'forgot_password.html' + chr(39) + ')'
    content += addon
    with open('app/routes/auth.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK')
else:
    print('Уже есть')