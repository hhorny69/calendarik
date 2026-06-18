with open("calendarik/app/routes/admin.py", "r", encoding="utf-8") as f:
    content = f.read()

first = content.find("def get_organizer_requests")
second = content.find("def get_organizer_requests", first+1)

# Найдем начало второго блока (декоратор перед ним)
block_start = content.rfind("@admin_bp.route", 0, second)

# Найдем начало следующей функции после второго
next_func = content.find("\n@admin_bp.route", second)

content = content[:block_start] + content[next_func:]

with open("calendarik/app/routes/admin.py", "w", encoding="utf-8") as f:
    f.write(content)
print("OK")
