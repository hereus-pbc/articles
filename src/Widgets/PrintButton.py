from bevyframe.Widgets.Templates.Containers import Box
from bevyframe.Widgets.Templates.Texts import SubTitle, Label
from bevyframe.Widgets.Style import Margin, Size, Cursor


class PrintButton(Box):
    def __init__(self, con, p) -> None:
        regular = con.app.db.query(con.env['db']['publishing']).filter_by(id=p.associated_to).first()
        if p.published:
            text = f"Part of {regular.title}, Published on {p.date.strftime('%B %d, %Y')}"
        else:
            text = f"Part of {regular.title}, Not yet published"
        super().__init__(
            childs=[
                SubTitle(p.title),
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
            onclick=con.start_redirect(f"/Library/Print.py?id={p.id}" if p.published else f"/Library/PrintStudio.py?id={p.id}"),
            cursor=Cursor.pointer
        )
