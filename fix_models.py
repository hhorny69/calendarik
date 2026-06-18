with open("calendarik/app/models.py", "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace(
    "    created_at = db.Column(db.DateTime, default=datetime.utcnow)\n    events",
    "    created_at = db.Column(db.DateTime, default=datetime.utcnow)\n    organizer_request = db.Column(db.String(20), default=None)\n    events"
)
with open("calendarik/app/models.py", "w", encoding="utf-8") as f:
    f.write(content)
print("OK")
