from TheProtocols import *
from bevyframe import *
from datetime import datetime, UTC
import pycountry
from Widgets.ArticleButton import ArticleButton


def get(con: Context) -> dict:
    addr = con.query.get('addr', con.email)
    articles = [article for article in con.app.db.query(con.env['db']['articles']).filter_by(author=addr).all() if not article.unpublished]
    return {
        'status': 'success',
        'addr': addr,
        'articles': [
            {
                'id': article.id,
                'title': article.title,
                'author': article.author,
                'date': article.date.strftime('%B %d, %Y'),
                'topic': article.topic,
                'signature': article.signature,
                'license': article.license,
            }
            for article in articles
        ]
    }
