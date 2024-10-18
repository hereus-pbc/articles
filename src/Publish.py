from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from datetime import datetime, UTC
from TheProtocols import *
from bevyframe import *
import json
import re


def check_html(content: str) -> bool:
    allowed_tags = [
        'p',
        'br',
        'span',
        'b',
        'i',
        'u',
        'strong',
        'em',
        'img',
        'a',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'ul',
        'ol',
        'li',
        'blockquote',
        'code',
        'pre',
    ]
    allowed_attributes = [
        'href',
        'src',
        'alt',
        'title',
        'class',
        'style'
    ]
    tag_re = re.compile(r'<(\/?)(\w+)([^>]*?)>')
    for match in tag_re.finditer(content):
        tag = match.group(2).lower()
        if tag not in allowed_tags:
            print(f" {tag} ", end='', flush=True)
            return False
        attr_re = re.compile(r'(\w+)=["\'](.*?)["\']')
        for attr_match in attr_re.finditer(match.group(3)):
            attr = attr_match.group(1).lower()
            if attr not in allowed_attributes:
                print(f" {attr} ", end='', flush=True)
                return False

    return True


@login_required
def post(con: Context) -> (Response, Page):
    title = con.query.get('title')
    notes = Notes(con.user)
    content = notes.get(f"Articles/Drafts/{title}")
    if not check_html(content):
        con.env['toast']['set'](con, 'Invalid HTML content')
        return con.start_redirect('/')
    privkey = load_pem_private_key(con.user.id.rsa_private_key.encode(), password=None, backend=default_backend())
    now = datetime.now(UTC)
    topic = ''  # con.form.get('topic')
    license = con.form.get('license')
    con.app.db.add(con.env['db']['articles'](
        title=title,
        content=content,
        author=con.email,
        date=now,
        topic=topic,
        license=license,
        unpublished='',
        signature=privkey.sign(
            json.dumps({
                'title': title,
                'content': content,
                'author': con.email,
                'date': now.strftime('%B %d, %Y'),
                'license': license
            }).encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        ).hex()
    ))
    con.app.db.commit()
    return con.start_redirect('/')


@login_required
def get(r: Context) -> Page:
    title = r.query.get('title')
    notes = Notes(r.user)
    content = notes.get(f"Articles/Drafts/{title}")
    word_count = len(content.split())
    return Page(
        title="HereUS Articles",
        color=r.user.id.settings.theme_color,
        childs=[
            r.env['sidebar'](r),
            r.env['topbar'](r, ''),
            Root([
                Box(
                    width=Size.max_content,
                    padding=Padding(bottom=Size.pixel(15)),
                    childs=[
                        Title(f'Publishing "{title}"'),
                        Label("<b>Word Count:</b> " + str(word_count)),
                        Form(
                            method='POST',
                            childs=[
                                Line([Widget(
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
                                )]),
                                Line(
                                    [
                                        'By clicking \'Publish\', you are accepting ',
                                        Link('Terms of Publishing', '/About/ToP.py')
                                    ],
                                    text_align=Align.center,
                                    width=Size.percent(100)
                                ),
                                Button(innertext="Publish", width=Size.percent(100)),
                            ]
                        )
                    ]
                )
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            ))
        ]
    )
