from TheProtocols import *
from bevyframe import *
from datetime import datetime, UTC
import pycountry
from Widgets.ArticleButton import ArticleButton


@login_required
def get(con: Context) -> (Page, dict):
    addr = con.query.get('addr', con.email)
    articles = [article for article in con.app.db.query(con.env['db']['articles']).filter_by(author=addr).all() if not article.unpublished]
    user = con.env['get_user'](addr)
    bd = datetime.strptime(user.birthday, "%Y-%m-%d")
    now = datetime.fromisoformat(datetime.now().isoformat())
    age = now.year - bd.year
    if now.month < bd.month or (now.month == bd.month and now.day < bd.day):
        age -= 1
    country = pycountry.countries.get(alpha_2=user.country).official_name
    pronouns = {
        'Male': 'he/him',
        'Female': 'she/her',
        'Gay': 'he/him',
        'Lesbian': 'she/her',
    }.get(user.gender, "they/them")
    return Page(
        title="HereUS Articles",
        color=con.user.id.settings.theme_color,
        childs=[
            con.env['sidebar'](con),
            con.env['topbar'](con, ''),
            Root([
                Image(
                    src=user.profile_photo,
                    alt="Profile Picture",
                    width=Size.pixel(100),
                    height=Size.pixel(100),
                ),
                Title(str(user)),
                Label(user.email, font_size=Size.Relative.font(0.8), color=Color.hex('80808080'), margin=Margin(top=Size.pixel(-30))),
                Bold("Location"),
                Label(country, margin=Margin(top=Size.pixel(-5))),
                Bold("Birthday"),
                Label(f"{bd.strftime('%B %d, %Y')} ({age} years old)", margin=Margin(top=Size.pixel(-5))),
                Bold("Pronouns"),
                Label(pronouns, margin=Margin(top=Size.pixel(-5))),
                Bold("Work"),
                Label("Not Available", margin=Margin(top=Size.pixel(-5))),
                Bold("Education"),
                Label("Not Available", margin=Margin(top=Size.pixel(-5))),
                Bold("Phone"),
                Label(user.phone_number, margin=Margin(top=Size.pixel(-5))),
                Bold("Social"),
                Label("Not Available", margin=Margin(top=Size.pixel(-5))),
                Button('mini', innertext=(
                    'Unfollow' if addr in con.data.get('following', []) else 'Follow'
                ), onclick=f"follow(this, '{addr}')"),
                Container([
                    ArticleButton(con, article)
                    for article in articles
                ], margin=Margin(top=Size.pixel(10))),
            ], margin=Margin(
                left=Size.pixel(100),
                top=Size.pixel(80),
            )),
            Widget(
                'script',
                innertext="""
                    const follow = (e, addr) => {
                        let b = e.innerHTML;
                        e.innerHTML = 'Processing...';
                        fetch(`/Backend/Follow.py?addr=${addr}`)
                        .then(async res => {
                            if (res.status === 200) { return res.json(); }
                            else { document.body.innerHTML = await res.text(); }
                        })
                        .then(data => {
                            if (data.status === 'followed') {
                                e.innerHTML = 'Unfollow';
                            } else if (data.status === 'unfollowed') {
                                e.innerHTML = 'Follow';
                            } else {
                                e.innerHTML = b;
                            }
                        })
                        .catch(err => {
                            console.error(err);
                        });
                    }
                """
            )
        ]
    )