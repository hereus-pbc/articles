from bevyframe import *
from TheProtocols import *
from datetime import datetime, UTC
import json


@login_required
def post(con: Context) -> (Response, Page):
    p = con.app.db.query(con.env['db']['published']).filter_by(id=con.query.get('id')).first()
    if p.published:
        return con.start_redirect(f'/Library/Print.py?id={p.id}')
    if ['title', 'license'] == list(con.form.keys()):
        p.title = con.form.get('title')
        p.license = con.form.get('license')
        con.app.db.commit()
        return get(con)
    else:
        regular = con.app.db.query(con.env['db']['publishing']).filter_by(id=p.associated_to).first()
        p.published = True
        p.date = datetime.now(UTC)
        p.signature = con.user.sign(json.dumps({
            'cover': p.cover,
            'associated_to': p.associated_to,
            'title': p.title,
            'date': p.date.strftime('%B %d, %Y'),
            'license': p.license,
            'articles': [i.article for i in con.app.db.query(con.env['db']['articles_published']).filter_by(published=p.id).all()]
        }))
        return con.start_redirect(f'/Library/Regular.py?id={regular.id}')


@login_required
def get(con: Context) -> Page:
    p = con.app.db.query(con.env['db']['published']).filter_by(id=con.query.get('id')).first()
    regular = con.app.db.query(con.env['db']['publishing']).filter_by(id=p.associated_to).first()
    articles = [con.app.db.query(con.env['db']['articles']).filter_by(id=i.article).first()
                for i in con.app.db.query(con.env['db']['articles_published']).filter_by(published=p.id).all()]
    return Page(
        title="Search - HereUS Articles",
        color=con.user.id.settings.theme_color,
        childs=[
            con.env['sidebar'](con),
            con.env['topbar'](con, ''),
            Root([
                Title('Print Studio'),
                Box(
                    width=Size.max_content,
                    padding=Padding(bottom=Size.pixel(15)),
                    css={'float': 'left'},
                    margin=Margin(right=Size.pixel(10)),
                    childs=[
                        Title('Edit Print'),
                        Form(
                            method='POST',
                            childs=[
                                Label('Title'),
                                Textbox('title', value=p.title),
                                Label('License'),
                                Line([Widget(
                                    'select',
                                    name='license',
                                    selector='textbox',
                                    css={'-webkit-appearance': 'none'},
                                    max_width=Size.percent(100),
                                    width=Size.percent(100),
                                    childs=[
                                        Widget('option', value=i[0], innertext=i[1], selected=i[0] == p.license)
                                        for i in [
                                            ('CC BY 4.0', 'Creative Commons'),
                                            ('CC BY-SA 4.0', 'CC Share Alike'),
                                            ('CC BY-ND 4.0', 'CC No Derivatives'),
                                            ('CC BY-NC 4.0', 'CC Non-Commercial'),
                                            ('CC BY-NC-ND 4.0', 'CC Non-Commercial, No Derivatives'),
                                            ('CC BY-NC-SA 4.0', 'CC Non-Commercial, Share-Alike'),
                                            ('CC0 1.0', 'Public Domain'),
                                        ]
                                    ]
                                )]),
                                Button(innertext="Edit", width=Size.percent(100)),
                            ]
                        )
                    ]
                ),
                Box(
                    width=Size.max_content,
                    padding=Padding(bottom=Size.pixel(15)),
                    css={'float': 'left'},
                    childs=[
                        Title('Articles'),
                        Container([
                            Label(f'{i.title} <a style="color:#80808080;">by</a> {con.env["get_user"](i.author)}', onclick=f"delete({i.id})")
                            for i in articles
                        ])
                    ]
                ),
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            )),
            Form(
                method='POST',
                childs=[
                    FAB(
                        onclick='',
                        childs=[Icon('globe_book')],
                        id='publish_button',
                        font_size=Size.Relative.font(2),
                    )
                ]
            )
        ]
    )
