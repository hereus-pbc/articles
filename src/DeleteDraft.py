from bevyframe import *
from TheProtocols import *


@login_required
def get(r: Context) -> Response:
    title = r.query.get('title').replace('/', '')
    notes = Notes(r.user)
    notes.delete(f"/Articles/Drafts/{title}")
    r.env['toast']['set'](r, 'Draft successfully deleted.')
    return r.start_redirect('/')
