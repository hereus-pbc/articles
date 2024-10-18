from bevyframe import *
from Widgets.ArticleButton import ArticleButton
from Widgets.PrintButton import PrintButton
from Widgets.RegularButton import RegularButton


def check_if_matches(text: str, piece: str) -> float:
    text: list[str] = text.split(' ')
    piece: list[str] = piece.split(' ')
    matches = 0
    for i in text:
        for j in piece:
            if i.lower() == j.lower():
                matches += 1
    return float(matches) / float(len(text))


@login_required
def get(con: Context) -> Page:
    query: str = con.query.get('q')
    temperature: float = 0.2
    article_results: list = []
    for article in con.app.db.query(con.env['db']['articles']).all():
        if not article.unpublished:
            if check_if_matches(" ".join([article.title, article.content]), query) >= temperature:
                article_results.append(article)
            elif query == article.author:
                article_results.append(article)
    user_results: dict = {}
    if '@' in query and ' ' not in query:
        user_results.update({query: con.env['get_user'](query)})
    else:
        for i in con.env['reverse_user_search'](query):
            user_results.update({i: con.env['get_user'](i)})
    publishing_results: list = []
    for publishing in con.app.db.query(con.env['db']['publishing']).all():
        if check_if_matches(" ".join([publishing.title, publishing.description]), query) >= temperature:
            publishing_results.append(publishing)
        elif query == publishing.manager:
            publishing_results.append(publishing)
    published_results: list = []
    return Page(
        title="Search - HereUS Articles",
        color=con.user.id.settings.theme_color,
        childs=[
            con.env['sidebar'](con),
            con.env['topbar'](con, query),
            Root([
                SubTitle('Articles') if article_results else '',
                Container([
                    ArticleButton(con, article)
                    for article in article_results
                ]),
                SubTitle('Regular Press') if publishing_results else '',
                Container([
                    RegularButton(con, publishing)
                    for publishing in publishing_results
                ]),
                SubTitle('Prints') if published_results else '',
                Container([
                    PrintButton(con, published)
                    for published in published_results
                ]),
                SubTitle('Users') if user_results else '',
                Container([
                    Line([
                        Link(user_results[user], f"/Profile.py?addr={user}", text_decoration='underline')
                    ], margin=Margin(left=Size.pixel(5)))
                    for user in user_results
                ]),
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            )),
        ]
    )