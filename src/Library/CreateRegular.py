from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from datetime import datetime, UTC
from bevyframe import *
import json


def post(con: Context) -> (Response, Page):
    privkey = load_pem_private_key(con.user.id.rsa_private_key.encode(), password=None, backend=default_backend())
    now = datetime.now(UTC)
    kwargs = {
        'title': con.form.get('title'),
        'manager': con.email,
        'date': now,
        'description': con.form.get('description'),
        'image': '',
        'banner': '',
        'signature': privkey.sign(
            json.dumps({
                'title': con.form.get('title'),
                'manager': con.email,
                'date': now.strftime('%B %d, %Y'),
                'description': con.form.get('description'),
                'image': '',
                'banner': '',
                'license': con.form.get('license')
            }).encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        ).hex(),
        'license': con.form.get('license')
    }
    con.app.db.add(con.env['db']['publishing'](**kwargs))
    con.app.db.add(con.env['db']['subscription'](
        email=con.email,
        regular=con.app.db.query(con.env['db']['publishing']).filter_by(**kwargs).first().id
    ))
    con.app.db.commit()
    con.env['toast']['set'](con, 'Publishing created')
    return con.start_redirect('/Library')


def get(con: Context) -> Page:
    return Page(
        title='HereUS Articles',
        color=con.user.id.settings.theme_color,
        childs=[
            con.env['sidebar'](con),
            con.env['topbar'](con, ''),
            Root([
                Box(
                    width=Size.max_content,
                    padding=Padding(bottom=Size.pixel(15)),
                    childs=[
                        Form(
                            method='POST',
                            childs=[
                                Title('Create a Regular Publishing'),
                                Label('Title'),
                                Textbox('title'),
                                Label('Description'),
                                Textbox('description'),
                                Label('License'),
                                Widget(
                                    'select',
                                    name='license',
                                    selector='textbox',
                                    css={'-webkit-appearance': 'none'},
                                    max_width=Size.percent(100),
                                    width=Size.percent(100),
                                    childs=[
                                        Widget('option', value=i[0], innertext=i[1])
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
                                ),
                                Line(
                                    [
                                        'By clicking \'Publish\', you are accepting ',
                                        Link('Terms of Publishing', '/About/ToP.py')
                                    ],
                                    text_align=Align.center,
                                    width=Size.percent(100)
                                ),
                                Button(innertext="Create", width=Size.percent(100)),
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