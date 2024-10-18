from bevyframe import *
from TheProtocols import *


@login_required
def post(r: Context) -> Response:
    id: int = int(r.query.get('id', -1))
    article = r.app.db.query(r.env['db']['articles']).filter_by(id=id).first()
    article.unpublished = f"by the author. Reason stated as: {r.json.get('reason', '')[:1].lower()}{r.json.get('reason', '')[1:]}"
    r.app.db.commit()
    r.env['toast']['set'](r, 'Article unpublished')
    return r.create_response()
