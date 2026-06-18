with open('app/static/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '.site-footer { margin-top: auto; ',
    '.site-footer { margin-top: 0; '
)

content = content.replace(
    '.page-wrapper {',
    '.page-wrapper { margin-bottom: 0; padding-bottom: 0;'
)

with open('app/static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')