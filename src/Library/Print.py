from bevyframe import *
from TheProtocols import User
from Widgets.ArticleButton import ArticleButton


def get(r: Context, id: int = None) -> Page:
    p = r.app.db.query(r.env['db']['published']).filter_by(id=r.query.get('id')).first()
    articles = [
        r.app.db.query(r.env['db']['articles']).filter_by(id=i.article).first()
        for i in r.app.db.query(r.env['db']['articles_published']).filter_by(published=p.id).all()
    ]
    return Page(
        title="HereUS Articles",
        color=r.user.id.settings.theme_color,
        childs=[
            Button(
                'mini',
                innertext='Information, Decentralized. Login now!',
                onclick=r.start_redirect('/Login.py'),
                width=Size.Viewport.width(100),
                position=Position.fixed(
                    top=Size.pixel(0),
                    right=Size.pixel(0),
                    left=Size.pixel(0),
                ),
                border_radius=Size.pixel(0),
            )
            if r.email.split('@')[0] == 'Guest' else
            Button(
                'mini',
                innertext=Icon('arrow_back'),
                onclick='window.history.back()',
                width=Size.fit_content,
                position=Position.fixed(
                    top=Size.pixel(10),
                    left=Size.pixel(10),
                ),
            ),
            Container(
                width=Size.pixel(600),
                margin=Margin(
                    top=Size.pixel(50),
                    left=Size.auto,
                    right=Size.auto,
                ),
                childs=[
                    Title(p.title),
                    Container([
                        ArticleButton(r, article)
                        for article in articles
                    ])
                ],
            ),
            Widget('script', innertext='''
                const bookmark = (id) => {
                    fetch(`/Backend/Bookmark.py?id=${id}`).then((data) => {
                    if (data.status === 200) { alert('Bookmarked!'); }
                    else { alert('Failed to bookmark!'); }
                    });
                }
                const unpublish = (id) => {
                    if (confirm('Are you sure you want to unpublish this article?')) {
                        fetch(`/Backend/Unpublish.py?id=${id}`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                'reason': prompt('Reason for unpublishing:')
                            })
                        }).then((data) => {
                            if (data.status === 200) { window.location.href = '/'; }
                            else { alert('Failed to unpublish!'); }
                        });
                    }
                }
            ''')
        ]
    )
