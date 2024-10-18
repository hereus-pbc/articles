from bevyframe import *
from Widgets.ArticleButton import ArticleButton


@login_required
def get(r: Context) -> Page:
    contacts = r.user.request('list_contacts').json().keys()
    return Page(
        title="HereUS Articles",
        color=r.user.id.settings.theme_color,
        childs=[
            r.env['sidebar'](r),
            r.env['topbar'](r, ''),
            Root([
                Title("From Your Contacts"),
                Container([
                    ArticleButton(r, article)
                    for article in r.app.db.query(r.env['db']['articles']).all() if article.author in contacts and not article.unpublished
                ]),
                Label("That's all!"),
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            ))
        ]
    )
