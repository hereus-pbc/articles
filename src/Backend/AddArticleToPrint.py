from bevyframe import *


@login_required
def post(con: Context) -> (Response, Page):
    article = con.app.db.query(con.env['db']['articles']).filter_by(id=con.query.get('id')).first()
    con.app.db.add(con.env['db']['articles_published'](
        article=con.query.get('id'),
        published=con.form.get('name'),
        permission=article.license.startswith('CC'),
    ))
    con.app.db.commit()
    return con.start_redirect(f'/Library/PrintStudio.py?id={con.form.get("name")}')


@login_required
def get(con: Context) -> Page:
    regulars = con.app.db.query(con.env['db']['publishing']).filter_by(manager=con.email).all()
    prints = []
    for i in regulars:
        prints += con.app.db.query(con.env['db']['published']).filter_by(associated_to=i.id).all()
    return Page(
        title="Search - HereUS Articles",
        color=con.user.id.settings.theme_color,
        childs=[
            con.env['sidebar'](con),
            con.env['topbar'](con, ''),
            Root([
                Box(
                    width=Size.max_content,
                    padding=Padding(bottom=Size.pixel(15)),
                    childs=[
                        Title('Add To Print'),
                        Form(
                            method='POST',
                            childs=[
                                Line([Widget(
                                    'select',
                                    name='name',
                                    selector='textbox',
                                    css={'-webkit-appearance': 'none'},
                                    max_width=Size.percent(100),
                                    width=Size.percent(100),
                                    childs=[
                                        Widget('option', value=i.id, innertext=i.title)
                                        for i in prints if not i.published
                                    ]
                                )]),
                                Button(innertext="Add"),
                            ]
                        )
                    ]
                )
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            )),
        ]
    )
