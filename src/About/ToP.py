from bevyframe import *
from TheProtocols import User

text = lambda r: f"""
""".strip()


@login_required
def get(r: Context) -> Page:
    return Page(
        title="HereUS Articles",
        color=r.user.id.settings.theme_color,
        childs=[
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
            Root([
                Title("Terms of Publishing"),
                Container([
                    Label(i)
                    for i in text(r).replace('    ', '').replace('  ', ' ').split('\n\n')
                ]),
            ], margin=Margin(
                top=Size.pixel(50),
            )),
        ]
    )