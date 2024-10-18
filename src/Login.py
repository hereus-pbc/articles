from bevyframe import *


def post(r: Context) -> (Page, Response):
    resp = r.start_redirect('/')
    if resp.login(r.form['email'], r.form['password']):
        return resp
    else:
        return get(r)


def get(r: Context) -> Page:
    return Page(
        title="HereUS Articles",
        color=Theme.blank,
        childs=[
            Root([
                Form(
                    method='POST',
                    childs=[
                        Title('Login'),
                        Line([Textbox('email', type='email', placeholder='email')]),
                        Line([Textbox('password', type='password', placeholder='password')]),
                        Line([Button(innertext='Login')])
                    ]
                )
            ])
        ]
    )
        