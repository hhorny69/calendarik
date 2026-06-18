with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<footer class=' + chr(39) + 'site-footer' + chr(39) + '>',
    '<footer class=' + chr(39) + 'site-footer' + chr(39) + ' style=' + chr(39) + 'margin-top:0;' + chr(39) + '>'
)
content = content.replace(
    '<div class=' + chr(39) + 'page-wrapper' + chr(39),
    '<div class=' + chr(39) + 'page-wrapper' + chr(39) + ' style=' + chr(39) + 'padding-bottom:0; margin-bottom:0;' + chr(39)
)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')