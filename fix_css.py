with open('app/static/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

if 'body {' not in content:
    content = 'body { margin: 0; padding: 0; background-color: #e8e0d8; display: flex; flex-direction: column; min-height: 100vh; }' + chr(10) + content

content = content.replace(
    '.site-footer {',
    '.site-footer { margin-top: auto; '
).replace(
    '.site-footer { margin-top: auto;  margin-top: auto; ',
    '.site-footer { margin-top: auto; '
)

with open('app/static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')