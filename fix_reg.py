with open("calendarik/templates/auth/register.html", "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace(
    "<option value='organizer'>Организатор</option>\n                        <option value='admin'>Администратор</option>",
    "<option value='organizer'>Организатор (требует одобрения админа)</option>"
)
with open("calendarik/templates/auth/register.html", "w", encoding="utf-8") as f:
    f.write(content)
print("OK")
