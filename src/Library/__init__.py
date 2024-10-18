from bevyframe import *
from TheProtocols import *
# noinspection PyUnresolvedReferences
from Widgets.ArticleButton import ArticleButton
# noinspection PyUnresolvedReferences
from Widgets.RegularButton import RegularButton



@login_required
def get(con: Context) -> Page:
    articles = []
    notes = Notes(con.user)
    for i in notes.fs['Articles']['Downloaded']:
        id = notes.fs['Articles']['Downloaded'][i].split(' by ')[0].strip('<!--')
        article = con.env['get_article'](notes, con, id, i)
        if article:
            articles.append(article)
    subscriptions = [i.regular for i in con.app.db.query(con.env['db']['subscription']).filter_by(email=con.email).all()]
    return Page(
        title="HereUS Articles",
        color=con.user.id.settings.theme_color,
        childs=[
            con.env['sidebar'](con),
            con.env['topbar'](con, ''),
            Root([
                Title("Saved Articles"),
                Label("These articles are uploaded to your network and durable to unpublish.", margin=Margin(top=Size.pixel(-20))),
                Container([
                    ArticleButton(con, article)
                    for article in articles
                ]),
                Title("Subscribed Regular Prints"),
                Label("These are the prints you are subscribed, they are sent to your mailbox regularly.", margin=Margin(top=Size.pixel(-20))),
                Container([
                    RegularButton(con, regular)
                    for regular in con.app.db.query(con.env['db']['publishing']).all() if regular.id in subscriptions
                ]),
                Label("That's all!"),
                Link('Manage Storage', '/Library/Storage.py', text_decoration='underline'),
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            )),
            FAB(
                onclick=con.start_redirect('/Library/CreateRegular.py'),
                childs=[Icon('add')],
                font_size=Size.Relative.font(2),
            ),
        ]
    )