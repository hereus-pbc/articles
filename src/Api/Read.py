from bevyframe import *
from TheProtocols import User


def get(r: Context) -> dict:
    id: int = int(r.query.get('id', -1))
    if id == -1:
        raise Error404
    article = r.env['get_article'](None, r, id)
    if article is None:
        raise Error404
    elif not article:
        return {
            'unpublished': {
                'by': article.unpublished.split('By the ')[1].split('. Reason stated as: ')[0],
                'reason': article.unpublished.split('. Reason stated as: ')[1],
            },
        }
    return {
        'id': article.id,
        'title': article.title,
        'author': article.author,
        'date': article.date.strftime('%B %d, %Y'),
        'topic': article.topic,
        'signature': article.signature,
        'license': article.license,
        'content': article.content,
    }