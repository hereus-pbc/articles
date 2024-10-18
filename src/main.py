from datetime import datetime

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from TheProtocols import *
from bevyframe import *
import hereus_ui_3_2
import json
import os

tables = {}
messages = {}
users = {}


def get_user(email: str) -> str:
    if email not in users:
        users[email] = User(email)
    return users.get(email)


class SavedArticle:
    def __init__(self, data: dict) -> None:
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        self.date = datetime.strptime(data['date'], '%B %d, %Y')
        self.content = data['content']
        self.license = data['license']
        self.signature = data['signature']
        self.unpublished = data['unpublished']

    def __bool__(self) -> bool:
        return self.unpublished == ''


def get_article(notes, con: Context, id: int, title: str = None):
    article = con.app.db.query(con.env['db']['articles']).filter_by(id=id).first()
    if article is not None:
        if article.unpublished:
            unpublished = article.unpublished
        else:
            return article
    else:
        unpublished = 'System Error'
    if con.email.split('@')[0] == 'Guest':
        return article
    if notes is None:
        notes = Notes(con.user)
    if title is None:
        for i in notes.fs['Articles']['Downloaded']:
            if str(notes.fs['Articles']['Downloaded'][i]).startswith(f'<!--{id} by '):
                title = i
    if title is None:
        return article
    f = str(notes.fs['Articles']['Downloaded'][title])
    f = f.removeprefix('<!--' + str(id) + ' by ')
    author_email = f.split('-->')[0]
    f = f.removesuffix('''-->
<p>
<em>
    This note is created automatically to save the article below.
    Unless you get explicit permission from the author, the license of the article applies.
</em>
</p>
<p><em>Article "''')
    title = f.split('" by ')[0]
    f = f.removeprefix(title + '" by ')
    author = f.split(' is licensed under ')[0]
    f = f.removeprefix(author + ' is licensed under ')
    license = f.split("</em></p>")[0]
    f = f.removeprefix(license + """</em></p>
<p><em>Signature: """)
    signature = f.split('</em></p>')[0]
    f = f.removeprefix(signature + """</em></p>
<p>By """)
    if author == f.split(' on ')[0]:
        f = f.removeprefix(author + ' on ')
        date = f.split('</p>')[0]
        f = f.removeprefix(date + '</p>\n<h1>')
        title = f.split('</h1>')[0]
        f = f.removeprefix(title + '</h1>\n<div>')
        content = f.split('</div>')[0]
        f = f.removeprefix(content + '</div>')
        if f == '':
            author_key = load_pem_public_key(con.env['get_user'](author_email).rsa_public_key.encode(), default_backend())
            try:
                author_key.verify(
                    bytes.fromhex(signature),
                    json.dumps({
                        'title': title,
                        'content': content,
                        'author': author_email,
                        'date': date,
                        'license': license
                    }).encode(),
                    padding.PKCS1v15(),
                    hashes.SHA256()
                )
                return SavedArticle(data={
                    'id': id,
                    'title': title,
                    'author': author_email,
                    'date': date,
                    'content': content,
                    'license': license,
                    'signature': signature,
                    'unpublished': unpublished
                })
            except InvalidSignature:
                pass


def get_message(con: Context) -> str:
    return messages.pop(con.email, None)


def set_message(con: Context, msg: str):
    messages[con.email] = msg


def sidebar(con: Context) -> Navbar:
    r = Navbar([
        NavItem(Icon('home'), '/', 'Home', active=(con.path == '/' or con.path.startswith('/Feeds'))),
        NavItem(Icon('newsstand'), '/Library', 'Regular Publishing', active=con.path.startswith('/Library')),
        # NavItem(Icon('store'), '/Store.py', 'Store', active=con.path.startswith('/Store.py')),
    ])
    r.style['margin-top'] = '50px'
    r.style['height'] = 'max-content'
    r = r.render() + Link(
        'See how your data is managed',
        '/About/DataManagement.py',
        text_decoration='underline',
        position=Position.fixed(
            bottom=Size.pixel(5),
            left=Size.pixel(5),
        ),
        font_size=Size.Relative.font(0.6),
    ).render()
    return r


def reverse_user_search(any=None, **kwargs) -> list[User]:
    r: list = []
    for j in users:
        user = users[j]
        if any:
            for i in user.__dict__:
                if str(any) in str(user.__dict__[i]):
                    r.append(j)
        else:
            for kwarg in kwargs:
                if hasattr(user, kwarg) and getattr(user, kwarg) and kwargs[kwarg] in getattr(user, kwarg):
                    r.append(j)
    return r


def environment() -> dict:
    r = {
        'get_article': get_article,
        'get_user': get_user,
        'sidebar': sidebar,
        'reverse_user_search': reverse_user_search,
        'topbar': lambda x, key: Container(
            position=Position.fixed(top=Size.pixel(0), left=Size.pixel(0), right=Size.pixel(0)),
            height=Size.pixel(70),
            id='topbar',
            css={'backdrop-filter': 'blur(10px)'},
            childs=[
                Container(
                    position=Position.fixed(top=Size.pixel(10), right=Size.pixel(10)),
                    onclick="window.location.href='/Profile.py'",
                    childs=[
                        Image(
                            x.user.id.profile_photo,
                            alt="Your Account",
                            height=Size.pixel(50),
                            width=Size.pixel(50),
                            border_radius=Size.percent(50)
                        )
                    ]
                ),
                Container(
                    width=substract_style(Size.Viewport.width(100), Size.pixel(180)),
                    max_width=Size.pixel(500),
                    position=Position.fixed(
                        top=Size.pixel(10),
                        left=Size.pixel(10)
                    ),
                    childs=[
                        Widget(
                            'form',
                            action='/Search.py',
                            method='GET',
                            childs=[
                                Textbox(
                                    selector="the_box",
                                    name='q',
                                    value=key,
                                    placeholder="Search...",
                                    border_radius=Size.pixel(50),
                                    width=Size.percent(100),
                                    max_width=Size.percent(100),
                                    height=Size.pixel(32),
                                    font_size=Size.Relative.font(1),
                                    padding=Padding(top=Size.pixel(6), left=Size.pixel(30)),
                                    margin=Margin(left=Size.pixel(80)),
                                    css={"border": "1px solid #808080A0"},
                                )
                            ]
                        )
                    ]
                ),
                Widget('script', innertext="""
                    document.getElementById('topbar').style.backgroundColor = window.getComputedStyle(document.body).backgroundColor;
                    document.getElementById('topbar').style.backgroundColor = document.getElementById('topbar').style.backgroundColor.replace(')', ', 0.9)');
                """)
            ]
        ),
        'db': tables,
        'toast': {
            'get': get_message,
            'set': set_message
        }
    }
    return r


app = Frame(
    package="net.hereus.articles",
    developer="hereus@hereus.net",
    administrator=False,
    secret=os.environ.get('SECRET'),
    style=hereus_ui_3_2,
    icon="https://static.hereus.net/favicon.png",
    keywords=[],
    permissions=[
        Permission.ID.RSA,
        Permission.ID.HiddenInformation,
        Permission.Chat,
        Permission.Contacts,
        Permission.Notes,
        Permission.Search
    ],
    environment=environment
)
db = Database(app, 'sqlite:///../articles.db')


class Articles(app.db.Model):
    __tablename__ = 'articles'
    id = DataTypes.Column(DataTypes.Integer, primary_key=True)
    title = DataTypes.Column(DataTypes.String)
    content = DataTypes.Column(DataTypes.String)
    author = DataTypes.Column(DataTypes.String)
    date = DataTypes.Column(DataTypes.Datetime)
    topic = DataTypes.Column(DataTypes.String)
    signature = DataTypes.Column(DataTypes.String)
    license = DataTypes.Column(DataTypes.String)
    unpublished = DataTypes.Column(DataTypes.String)

    def __bool__(self) -> bool:
        return self.unpublished == ''


class Publishing(app.db.Model):
    __tablename__ = 'publishing'
    id = DataTypes.Column(DataTypes.Integer, primary_key=True)
    title = DataTypes.Column(DataTypes.String)
    manager = DataTypes.Column(DataTypes.String)
    date = DataTypes.Column(DataTypes.Datetime)
    description = DataTypes.Column(DataTypes.String)
    image = DataTypes.Column(DataTypes.String)
    banner = DataTypes.Column(DataTypes.String)
    signature = DataTypes.Column(DataTypes.String)
    license = DataTypes.Column(DataTypes.String)


class Published(app.db.Model):
    __tablename__ = 'published'
    id = DataTypes.Column(DataTypes.Integer, primary_key=True)
    cover = DataTypes.Column(DataTypes.String)
    associated_to = DataTypes.Column(DataTypes.Integer)
    title = DataTypes.Column(DataTypes.String)
    published = DataTypes.Column(DataTypes.Bool)
    date = DataTypes.Column(DataTypes.Datetime)
    signature = DataTypes.Column(DataTypes.String)
    license = DataTypes.Column(DataTypes.String)


class ArticlesPublished(app.db.Model):
    __tablename__ = 'articles_published'
    id = DataTypes.Column(DataTypes.Integer, primary_key=True)
    article = DataTypes.Column(DataTypes.Integer)
    published = DataTypes.Column(DataTypes.Integer)
    permission = DataTypes.Column(DataTypes.Bool)


class Subscription(app.db.Model):
    __tablename__ = 'subscription'
    id = DataTypes.Column(DataTypes.Integer, primary_key=True)
    email = DataTypes.Column(DataTypes.String)
    regular = DataTypes.Column(DataTypes.Integer)


tables.update({
    'articles': Articles,
    'publishing': Publishing,
    'published': Published,
    'subscription': Subscription,
    'articles_published': ArticlesPublished
})

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=80, debug=True)
            