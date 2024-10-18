from bevyframe import *
from TheProtocols import *
import json


@login_required
def post(con: Context) -> dict:
    notes = Notes(con.user)
    data = con.json
    if data.get('event') == 'delete_draft':
        if notes.delete(f"/Articles/Drafts/{data.get('id')}"):
            return {'status': 'success'}
        else:
            return {'status': 'error'}
    if data.get('event') == 'delete_saved':
        if notes.delete(f"/Articles/Downloaded/{data.get('id')}"):
            return {'status': 'success'}
        else:
            return {'status': 'error'}
    elif data.get('event') == 'reset':
        con.data = {}
        con.preferences = {}
        return {'status': 'success'}
    return {'status': 'error'}


@login_required
def get(con: Context) -> Page:
    notes = Notes(con.user)
    used_net = len(json.dumps(notes.fs.get('Articles', {}))) - 2
    used_net += used_net + (len(json.dumps(dict(con.data))) - 2)
    used_net += used_net + (len(json.dumps(dict(con.preferences))) - 2)
    used_net = str(used_net / 1024)[:5]
    used_db = 0
    articles = con.app.db.query(con.env['db']['articles']).filter_by(author=con.email).all()
    for article in articles:
        if not article.unpublished:
            used_db += len(json.dumps({
                'id': int(article.id),
                'title': str(article.title),
                'content': str(article.content),
                'author': str(article.author),
                'date': article.date.strftime('%Y-%m-%d %H:%M:%S'),
                'topic': str(article.topic),
                'signature': str(article.signature),
                'license': str(article.license)
            }))
    publishings = con.app.db.query(con.env['db']['publishing']).filter_by(manager=con.email).all()
    for publishing in publishings:
        used_db += len(json.dumps({
            'id': int(publishing.id),
            'title': str(publishing.title),
            'manager': str(publishing.manager),
            'date': publishing.date.strftime('%Y-%m-%d %H:%M:%S'),
            'description': str(publishing.description),
            'image': str(publishing.image),
            'banner': str(publishing.banner),
            'signature': str(publishing.signature),
            'license': str(publishing.license)
        }))
    publisheds = con.app.db.query(con.env['db']['published']).filter_by(associated_to=con.email).all()
    for published in publisheds:
        used_db += len(json.dumps({
            'id': int(published.id),
            'associated_to': int(published.associated_to),
            'date': published.date.strftime('%Y-%m-%d %H:%M:%S'),
            'signature': str(published.signature),
            'license': str(published.license)
        }))
    used_db = str(used_db / 1024)[:5]
    return Page(
        title="HereUS Articles",
        color=con.user.id.settings.theme_color,
        childs=[
            con.env['sidebar'](con),
            con.env['topbar'](con, ''),
            Root([
                Title("Stored on Network Storage"),
                Label("HereUS Articles uses storage from your preferred network to provide you the control over your data.", margin=Margin(top=Size.pixel(-20))),
                Label(f"<b>Used:</b> {used_net} KB", margin=Margin(top=Size.pixel(-20))),
                Container([
                    Label(f"[Saved] {i}", text_decoration='underline', onclick=f"delete_saved(this, '{i}')", color=Color.red, cursor=Cursor.pointer)
                    for i in list(notes.fs.get('Articles', {}).get('Downloaded', {}).keys())
                ]),
                Container([
                    Label(f"[Draft] {i}", text_decoration='underline', onclick=f"delete_draft(this, '{i}')", color=Color.red, cursor=Cursor.pointer)
                    for i in list(notes.fs.get('Articles', {}).get('Drafts', {}).keys())
                ]),
                Label(f"App Data + Preferences", text_decoration='underline', onclick=f"reset(this)", color=Color.red, cursor=Cursor.pointer),
                Title("Stored on Central Database"),
                Label("HereUS Articles uses an internal database to serve your publishments to public even when you are offline.", margin=Margin(top=Size.pixel(-20))),
                Label(f"<b>Used:</b> {used_db} KB", margin=Margin(top=Size.pixel(-20))),
                Container([
                    Label(f"[Article] {i.title}")
                    for i in articles
                ]),
                Container([
                    Label(f"[Regular] {i.title}")
                    for i in publishings
                ]),
                Container([
                    Label(f"[Print] {i.associated_to} - {i.date.strftime('%Y-%m-%d %H:%M:%S')}")
                    for i in publisheds
                ]),
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            )),
            Widget('script', innertext='''
                const delete_draft = (e, id) => {
                    if (confirm("Are you sure you want to delete this draft?")) {
                        fetch('/Library/Storage.py', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                event: 'delete_draft',
                                id: id
                            })
                        }).then(response => response.json()).then(data => {
                            e.innerHTML = '<i>Deleted!</i>';
                            e.style.color = 'green';
                            e.onclick = null;
                        });
                    }
                }
                const delete_saved = (e, id) => {
                    if (confirm("Are you sure you want to delete this saved article? You will lose access to it if it's unpublished.")) {
                        fetch('/Library/Storage.py', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                event: 'delete_saved',
                                id: id
                            })
                        }).then(response => response.json()).then(data => {
                            e.innerHTML = '<i>Deleted!</i>';
                            e.style.color = 'green';
                            e.onclick = null;
                        });
                    }
                }
                const reset = (e, id) => {
                    if (confirm(
                        "Are you sure you want to reset this app? " + 
                        "This will reset all preferences, unfollow everyone, and clear interests." +
                        "Your drafts and published articles will not be affected."
                    )) {
                        fetch('/Library/Storage.py', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                event: 'reset',
                                id: id
                            })
                        }).then(response => response.json()).then(data => {
                            e.innerHTML = '<i>Done!</i>';
                            e.style.color = 'green';
                            e.onclick = null;
                        });
                    }
                }
            ''')
        ]
    )