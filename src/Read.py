from bevyframe import *
from TheProtocols import User


def get(r: Context) -> Page:
    id: int = int(r.query.get('id', -1))
    if id == -1:
        raise Error404
    article = r.env['get_article'](None, r, id)
    if article is None:
        raise Error404
    elif not article:
        return Page(
            title="Article Unpublished - HereUS Articles",
            color=r.user.id.settings.theme_color,
            childs=[
                '' if r.email.split('@')[0] == 'Guest' else
                r.env['sidebar'](r),
                Button(
                    'mini',
                    innertext='Information, Decentralized. Login now!',
                    onclick=r.start_redirect('/Login.py'),
                    width=Size.Viewport.width(100),
                    position=Position.fixed(
                        top=Size.pixel(0),
                        right=Size.pixel(0),
                        left=Size.pixel(0),
                    ),
                    border_radius=Size.pixel(0),
                )
                if r.email.split('@')[0] == 'Guest' else
                r.env['topbar'](r, ''),
                Root([
                    Title("This article has been unpublished."),
                    Label(f"The article you are looking for is unpublished {article.unpublished}."),
                ], margin=Margin(
                    left=Size.pixel(100),
                    top=Size.pixel(80),
                )),
            ]
        )
    user = r.env['get_user'](article.author)
    return Page(
        title="HereUS Articles",
        color=r.user.id.settings.theme_color,
        OpenGraph={
            'title': article.title,
            'description': f"By {user} on {article.date.strftime('%B %d, %Y')}",
            'image': '',
            'url': f"https://articles.hereus.net/Read.py?id={id}",
            'type': 'article',
        },
        author=str(user),
        childs=[
            Button(
                'mini',
                innertext='Information, Decentralized. Login now!',
                onclick=r.start_redirect('/Login.py'),
                width=Size.Viewport.width(100),
                position=Position.fixed(
                    top=Size.pixel(0),
                    right=Size.pixel(0),
                    left=Size.pixel(0),
                ),
                border_radius=Size.pixel(0),
            )
            if r.email.split('@')[0] == 'Guest' else
            Button(
                'mini',
                innertext=Icon('arrow_back'),
                onclick='window.history.back()',
                width=Size.fit_content,
                position=Position.fixed(
                    top=Size.pixel(10),
                    left=Size.pixel(10),
                ),
            ),
            '' if r.email.split('@')[0] == 'Guest' or article.unpublished else
            Button(
                'mini',
                innertext=Icon('bookmark'),
                onclick=f'bookmark({id})',
                width=Size.fit_content,
                position=Position.fixed(
                    top=Size.pixel(10),
                    left=Size.pixel(60),
                ),
            ),
            '' if r.email.split('@')[0] == 'Guest' else
            Button(
                'mini',
                innertext=Icon('add'),
                onclick=r.start_redirect(f'/Backend/AddArticleToPrint.py?id={id}'),
                width=Size.fit_content,
                position=Position.fixed(
                    top=Size.pixel(10),
                    left=Size.pixel(110),
                ),
            ),
            Button(
                'mini',
                innertext=Icon('archive'),
                background_color=Color.red,
                onclick=f'unpublish({id})',
                width=Size.fit_content,
                position=Position.fixed(
                    top=Size.pixel(10),
                    left=Size.pixel(160),
                ),
            ) if r.email == article.author and not article.unpublished else '',
            Label(
                f'Unpublished {article.unpublished}, reading from network',
                color=Color.red,
                position=Position.fixed(
                    top=Size.pixel(0),
                    left=Size.pixel(60),
                ),
            ) if article.unpublished else '',
            Root([
                Label(f"By {user} on {article.date.strftime('%B %d, %Y')}"),
                Title(article.title),
                Container([
                    Label(i) for i in article.content.split('\n')
                ]),
            ], margin=Margin(
                top=Size.pixel(50),
            )),
            Root([
                Label(
                    f"Article \"{article.title}\" by {user} is licensed under {article.license}",
                    css={'font-style': 'italic'}
                ),
                Title("About The Author", margin=Margin(top=Size.pixel(50))),
                Label(F"{user}, {user.email}"),
                Link(
                    "View more on profile",
                    f"/Profile.py?addr={article.author}",
                    text_decoration='underline'
                ),
            ], margin=Margin(
                top=Size.pixel(150),
            )),
            Widget('script', innertext='''
                const bookmark = (id) => {
                    fetch(`/Backend/Bookmark.py?id=${id}`).then((data) => {
                    if (data.status === 200) { alert('Bookmarked!'); }
                    else { alert('Failed to bookmark!'); }
                    });
                }
                const unpublish = (id) => {
                    if (confirm('Are you sure you want to unpublish this article?')) {
                        fetch(`/Backend/Unpublish.py?id=${id}`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                'reason': prompt('Reason for unpublishing:')
                            })
                        }).then((data) => {
                            if (data.status === 200) { window.location.href = '/'; }
                            else { alert('Failed to unpublish!'); }
                        });
                    }
                }
            ''')
        ]
    )
