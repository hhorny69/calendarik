with open("calendarik/app/routes/admin.py", "r", encoding="utf-8") as f:
    content = f.read()

# Найдем и удалим дубликат - первое вхождение get_organizer_requests
first = content.find("@admin_bp.route('/api/admin/organizer-requests', methods=['GET'])")
second = content.find("@admin_bp.route('/api/admin/organizer-requests', methods=['GET'])", first+1)

if second != -1:
    # Удаляем от первого до второго вхождения
    content = content[:first] + content[second:]
    print("Дубликат удален")
else:
    print("Дубликата нет")

with open("calendarik/app/routes/admin.py", "w", encoding="utf-8") as f:
    f.write(content)
