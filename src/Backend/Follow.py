from bevyframe import *
from TheProtocols import *


@login_required
def get(r: Context) -> dict:
    addr = r.query.get('addr', r.email)
    if 'following' not in r.data:
        r.data['following'] = []
    if addr in r.data.get('following'):
        r.data['following'].remove(addr)
        return {'status': 'unfollowed'}
    else:
        r.data['following'].append(addr)
        print(dict(r.data))
        return {'status': 'followed'}
