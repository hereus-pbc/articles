from bevyframe import *


@login_required
def get(r: Context) -> Page:
    return Page(
        title="Method Not Allowed - HereUS Articles",
        color=r.user.id.settings.theme_color,
        childs=[
            r.env['sidebar'](r),
            r.env['topbar'](r, ''),
            Root([
                Title("Oh no!"),
                Label("You found a page not yet completed. Please report it via email."),
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            )),
        ]
    )
