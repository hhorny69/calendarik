import re

with open("calendarik/templates/admin.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "<button class='admin-tab' onclick=\"showTab('events', this)\">Все мероприятия</button>",
    "<button class='admin-tab' onclick=\"showTab('events', this)\">Все мероприятия</button>\n        <button class='admin-tab' onclick=\"showTab('org-req', this)\">Заявки на организатора</button>"
)

content = content.replace("['users', 'pending', 'events']", "['users', 'pending', 'events', 'org-req']")

content = content.replace(
    "else if (tab === 'events') loadEvents();",
    "else if (tab === 'events') loadEvents();\n    else if (tab === 'org-req') loadOrgReq();"
)

new_funcs = """
async function loadOrgReq() {
    const r = await fetch('/api/admin/organizer-requests');
    const c = document.getElementById('org-req-container');
    if (!r.ok) { c.innerHTML = '<p style="color:#c0392b;text-align:center;">Нет доступа</p>'; return; }
    const users = await r.json();
    if (!users.length) { c.innerHTML = '<p style="color:#666;text-align:center;">Нет заявок</p>'; return; }
    var rows = users.map(u => '<tr><td>'+u.id+'</td><td>'+u.username+'</td><td>'+u.email+'</td><td>'+u.created_at+'</td><td style="display:flex;gap:6px;"><button class="btn btn-primary" style="width:auto;padding:6px 12px;font-size:12px;background:#27500a;border-color:#27500a" onclick="approveOrg('+u.id+')">Одобрить</button><button class="btn btn-danger" style="width:auto;padding:6px 12px;font-size:12px;" onclick="rejectOrg('+u.id+')">Отклонить</button></td></tr>').join('');
    c.innerHTML = '<table class="admin-table"><thead><tr><th>ID</th><th>Логин</th><th>Email</th><th>Дата</th><th>Действия</th></tr></thead><tbody>'+rows+'</tbody></table>';
}
async function approveOrg(id) { const r = await fetch('/api/admin/organizer-requests/'+id+'/approve',{method:'POST'}); if(r.ok) loadOrgReq(); }
async function rejectOrg(id) { const r = await fetch('/api/admin/organizer-requests/'+id+'/reject',{method:'POST'}); if(r.ok) loadOrgReq(); }
"""

tab_div = """
    <div id='tab-org-req' style='display:none;'>
        <div class='admin-card'>
            <div class='admin-card-title'>Заявки на роль организатора</div>
            <div id='org-req-container'><p style='color:#666; text-align:center;'>Загрузка...</p></div>
        </div>
    </div>
"""

content = content.replace('loadNavRole();', new_funcs + 'loadNavRole();')
content = content.replace('<script>', tab_div + '<script>', 1)

with open("calendarik/templates/admin.html", "w", encoding="utf-8") as f:
    f.write(content)
print("admin.html OK")
