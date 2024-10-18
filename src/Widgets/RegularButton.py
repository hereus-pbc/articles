from bevyframe.Widgets.Templates.Containers import Box
from bevyframe.Widgets.Templates.Texts import SubTitle, Label
from bevyframe.Widgets.Style import Margin, Size, Cursor


class RegularButton(Box):
    def __init__(self, con, publishing) -> None:
        text = f"By {con.env['get_user'](publishing.manager)} since {publishing.date.strftime('%B %Y')}"
        super().__init__(
            childs=[
                SubTitle(publishing.title),
                Label(
                    innertext=publishing.description,
                    margin=Margin(
                        top=Size.pixel(-20)
                    )
                ),
            ],
            margin=Margin(
                bottom=Size.pixel(10)
            ),
            onclick=con.start_redirect(f"/Library/Regular.py?id={publishing.id}"),
            cursor=Cursor.pointer
        )
