from bevyframe.Widgets.Templates.Containers import Box
from bevyframe.Widgets.Templates.Texts import SubTitle, Label
from bevyframe.Widgets.Style import Margin, Size, Cursor


class ArticleButton(Box):
    def __init__(self, con, article) -> None:
        text = f"By {con.env['get_user'](article.author)} on {article.date.strftime('%B %d, %Y')}"
        if hasattr(article, 'unpublished') and article.unpublished:
            text += ". unpublished"
        super().__init__(
            childs=[
                SubTitle(article.title),
                Label(
                    innertext=text,
                    margin=Margin(
                        top=Size.pixel(-20)
                    )
                ),
            ],
            margin=Margin(
                bottom=Size.pixel(10)
            ),
            onclick=con.start_redirect(f"/Read.py?id={article.id}"),
            cursor=Cursor.pointer
        )
