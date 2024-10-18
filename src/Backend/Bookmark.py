from bevyframe import *
from TheProtocols import *


@login_required
def get(r: Context) -> Response:
    id: int = int(r.query.get('id', -1))
    if id == -1:
        raise Error404
    notes = Notes(r.user)
    article = r.app.db.query(r.env['db']['articles']).filter_by(id=id).first()
    if article is None or article.unpublished:
        return r.create_response(status_code=500)
    user = r.env['get_user'](article.author)
    body = f"""
<!--{id} by {article.author}-->
<p>
    <em>
        This note is created automatically to save the article below.
        Unless you get explicit permission from the author, the license of the article applies.
    </em>
</p>
<p><em>Article "{article.title}" by {user} is licensed under {article.license}</em></p>
<p><em>Signature: {article.signature}</em></p>
<p>By {user} on {article.date.strftime('%B %d, %Y')}</p>
<h1>{article.title}</h1>
<div>{article.content}</div>
""".strip('\n')
    if notes.edit("/Articles/Downloaded/" + article.title, body):
        return r.create_response()
    else:
        return r.create_response(status_code=500)
