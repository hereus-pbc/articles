from bevyframe import *
from Widgets.ArticleButton import ArticleButton


@login_required
def get(r: Context) -> Page:
    contacts = r.user.request('list_contacts').json().keys()
    topics = r.data.get('topics', [])
    following = r.data.get('following', [])
    message = r.env['toast']['get'](r)
    contents_c, contents_f, contents_t = [
        ArticleButton(r, article)
        for article in r.app.db.query(r.env['db']['articles']).all()[:3]
        if article.author in contacts and not article.unpublished
    ], [
        ArticleButton(r, article)
        for article in r.app.db.query(r.env['db']['articles']).all()[:3]
        if article.author in following and not article.unpublished
    ], [
        ArticleButton(r, article)
        for article in r.app.db.query(r.env['db']['articles']).all()[:3] if article.topic in topics and not article.unpublished
    ]
    contents_c.reverse()
    contents_f.reverse()
    contents_t.reverse()
    return Page(
        title="HereUS Articles",
        color=r.user.id.settings.theme_color,
        childs=[
            r.env['sidebar'](r),
            r.env['topbar'](r, ''),
            Root([
                Title("From Your Contacts"),
                Container(contents_c),
                Button(innertext="View More", onclick=r.start_redirect('/Feeds/Contacts.py')),
                Title("From Who You Follow"),
                Container(contents_f),
                Button(innertext="View More", onclick=r.start_redirect('/Feeds/Follows.py')),
                # Title("About Your Topics"),
                # Container(contents_t),
                # Button(innertext="View More", onclick=r.start_redirect('/Feeds/Topics.py')),
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            )),
            FAB(
                onclick=r.start_redirect('/Write.py'),
                childs=[Icon('contract_edit')],
                font_size=Size.Relative.font(2),
            ),
            Box(
                id='toast',
                childs=[Label(message)],
                position=Position.fixed(
                    top=Size.pixel(10),
                    right=Size.pixel(10),
                ),
            ) if message is not None else '',
            Widget('script', innertext="""
                setTimeout(() => {
                    document.getElementById('toast').style.height = '1px';
                    document.getElementById('toast').style.width = '1px';
                    document.getElementById('toast').style.visibility = 'hidden';
                    document.getElementById('toast').style.display = 'none';
                }, 3000);
            """),
        ]
    )
        