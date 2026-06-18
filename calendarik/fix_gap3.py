with open('app/static/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'body { margin: 0; padding: 0; background-color: #8B1A2B; display: flex; flex-direction: column; min-height: 100vh; }',
    'body { margin: 0; padding: 0; background-color: #e8e0d8; }'
)

with open('app/static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')