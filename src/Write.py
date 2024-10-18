from bevyframe import *
from TheProtocols import *


@login_required
def post(r: Context) -> (Page, Response):
    notes = Notes(r.user)
    status = notes.edit(f"/Articles/Drafts/{r.form['title']}", r.form['content'])
    return get(r, saved=status)


@login_required
def get(r: Context, saved=True) -> Page:
    if not saved:
        title = r.form.get('title', '').replace('/', '')
    else:
        title = r.query.get('title', '').replace('/', '')
    notes = Notes(r.user)
    editables = list(notes.fs.get('Articles', {}).get('Drafts', {}).keys())
    if title == '' and len(editables) > 0:
        title = editables[0]
    if not saved:
        content = r.form.get('content', '')
    else:
        try:
            content = notes.get(f"Articles/Drafts/{title}")
        except NoteNotFound:
            content = ''
    message = r.env['toast']['get'](r)
    return Page(
        title="HereUS Articles",
        color=r.user.id.settings.theme_color,
        childs=[
            Button(
                selector="mini",
                innertext=Icon('arrow_back'),
                onclick=r.start_redirect('/'),
                width=Size.fit_content
            ),
            Root(
                childs=[
                    ('' if saved else Label("Network Error, couldn't save. Don't close tab.", color=Color.red))
                ] + (
                    [] if (len(editables) < 2 and (title == '' or title in editables)) else
                    [
                        Title("Drafts"),
                        Container(
                            childs=[
                                Widget(
                                    'p',
                                    cursor=Cursor.pointer,
                                    onclick=r.start_redirect(f'/Write.py?title={title}'),
                                    innertext=x,
                                )
                                for x in editables
                            ],
                            margin=Margin(bottom=Size.pixel(100)),
                        ),
                    ]
                ) + [
                    Form(
                        method='POST',
                        childs=[
                            Textbox(
                                'title',
                                background_color=Color.transparent,
                                css={'border': NoStyle, 'font-weight': 'bold'},
                                font_size=Size.Relative.font(2),
                                placeholder="Title",
                                width=Size.Viewport.width(90),
                                max_width=Size.pixel(1000),
                                value=title,
                            ),
                            TextArea(
                                'content',
                                innertext=content,
                                background_color=Color.transparent,
                                css={'border': NoStyle, 'resize': NoStyle},
                                font_size=Size.Relative.font(1),
                                height=Size.Viewport.height(70),
                                placeholder="Content",
                                width=substract_style(Size.Viewport.width(90), Size.pixel(20)),
                                max_width=Size.pixel(980),
                                padding=Padding(
                                    left=Size.pixel(10),
                                    right=Size.pixel(10),
                                    top=Size.pixel(10),
                                ),
                            ),
                            FAB(
                                onclick="save()",
                                childs=[Icon('save')],
                                font_size=Size.Relative.font(2),
                            )
                        ]
                    ),
                    FAB(
                        onclick=r.start_redirect(f'/DeleteDraft.py?title={title}'),
                        childs=[Icon('delete')],
                        id='delete_button',
                        font_size=Size.Relative.font(2),
                        margin=Margin(bottom=Size.pixel(120)),
                        background_color=Color.red,
                    ),
                    FAB(
                        onclick=r.start_redirect(f'/Publish.py?title={title}'),
                        childs=[Icon('globe_book')],
                        id='publish_button',
                        font_size=Size.Relative.font(2),
                        margin=Margin(bottom=Size.pixel(60)),
                    )
                ],
                margin=Margin(
                    left=Size.auto,
                    right=Size.auto,
                    top=Size.pixel(10),
                ),
                max_width=Size.pixel(1000),
                width=Size.Viewport.width(90),
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
                const unsaved = () => {
                    document.getElementById('delete_button').style.display = 'none';
                    document.getElementById('publish_button').style.display = 'none';
                };
                addEventListener("DOMContentLoaded", (event) => {
                    document.getElementById('title').addEventListener('input', unsaved);
                    document.getElementById('content').addEventListener('input', unsaved);
                });
            """),
        ]
    )
        