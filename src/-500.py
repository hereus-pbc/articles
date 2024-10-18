from bevyframe import *


@login_required
def get(r: Context) -> Page:
    return Page(
        title="System Error - HereUS Articles",
        color=r.user.id.settings.theme_color,
        childs=[
            r.env['sidebar'](r),
            r.env['topbar'](r, ''),
            Root([
                Title("Oh no!"),
                Label("An error occurred in the system. Please try again later."),
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            )),
        ]
    )
