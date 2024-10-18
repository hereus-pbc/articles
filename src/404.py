from bevyframe import *


def get(r: Context) -> (Page, Response):
    return Page(
        title="Article Not Found - HereUS Articles",
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
                Title("You got the wrong link."),
                Label("The article you are looking for does not exist."),
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            )),
        ]
    ) if r.path.startswith('/Read.py') else r.start_redirect('/')
