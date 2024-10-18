from bevyframe import *
from TheProtocols import *
from Widgets.PrintButton import PrintButton


@login_required
def get(con: Context) -> Page:
    regular = con.app.db.query(con.env['db']['publishing']).filter_by(id=con.query.get('id')).first()
    prints = con.app.db.query(con.env['db']['published']).filter_by(associated_to=con.query.get('id')).all()
    return Page(
        title="Search - HereUS Articles",
        color=con.user.id.settings.theme_color,
        childs=[
            con.env['sidebar'](con),
            con.env['topbar'](con, ''),
            Root([
                Title(regular.title),
                Label(regular.description, margin=Margin(top=Size.pixel(-20))),
                Label(f"Managed by {User(regular.manager)}", font_size=Size.Relative.font(0.8)),
                Container([PrintButton(con, p) for p in prints])
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            )),
            FAB(
                onclick=con.start_redirect(f'/Library/CreatePrint.py?regular={regular.id}'),
                childs=[Icon('add')],
                font_size=Size.Relative.font(2),
            ) if con.email == regular.manager else '',
        ]
    )