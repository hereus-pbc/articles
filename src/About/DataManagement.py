from bevyframe import *
from TheProtocols import User

text = lambda r: f"""
<h2>What is in Database?</h2>
<p>
    We store your articles in a database to provide you the service even when you are offline.
    
    More technically, we have 3 tables in our database:
    
    <ul>
        <li>Articles</li>
        <li>Journals</li>
        <li>Prints of Journals</li>
    </ul>
    
    In an article, we store the title, content, author, date, and license.
    In a journal, we store the title, manager, date, description, image, banner, and license.
    In a print of a journal, we store the associated journal, date, and license.
    
    Of course, we have rules to keep this place safe for everyone, so we can unpublish your articles if they violate our rules.
    However, you will always have access to the articles you saved as they are downloaded (technically uploaded, but this way is more understandable in traditional understanding) to your preferred network.
    Please note, we are unable to ban anyone since there is no central user system in our app.
    All user data comes from networks as you enter your email address and password to let system login.
    Also after you successfully log in, we do not store your password, all authentication is done using a token which is limited by permissions requested.
    
    Even though we would be happy if you just believe what we say, we know everyone can say these nice words, including liars.
    We believe empty making user just trust what company says is not a great approach of user-company relationship, so this app is open-source.
    You can check the source code of this app from <a href="https://github.com/hereus-pbc/articles" style="text-decoration:underline;">here</a>.
</p>
<h2>What is Stored on Network?</h2>
<p>
    First of all, we only fetch your theme color from the network, we have no over it as this app doesn't request permisssion to change it.
    
    We store your drafts as a note on your network to provide you the control over your data, this means you can actually edit them using any note editor.
    We also store your downloaded articles as notes on your network to provide you the access to them even they are unpublished.
    However, you shouldn't be editing an article you downloaded as it is a violation of the license of the article.
    If you are a typa person who doesn't care about licenses, system enforces it by adding signature of the article to the note.
    This way, you can't edit the article without changing the signature, which is impossible unless you are the author using this app.
    We have right to check if you violated any license with any request done to this app; however, we can't check if you don't use this app as we can't access your network without your constent, see tokens.
    
    In addition to these, we fetch your contacts from your network to provide you a feed.
    We also keep about who you follow and which topics you are interested in, stored on your network as app data.
    Technically you can edit any app data, legally you can't edit if ToS says you can't, so here is our consent:
    You can edit data saved by this app, but this doesn't mean we guarantee the app will work as expected after the modifications.
    So, you can edit data saved by this app with your own risk.
    
    Lastly, we fetch user IDs from their networks to provide user profiles.
    We can list all data set to public by a user, so we will.
    Do not ask us to hide your data, hide it from network settings instead.
    We do not store any of these data, we just fetch them from networks, we have no control over them.
</p>
<h2>Cookies!</h2>
<p>
    There is no cookies used by this app.
    There is only one cookie which is managed by the framework to keep you logged in.
    Take a look if you want:

    {';'.join(i + "=" + r.cookies[i] for i in r.cookies)};
</p>
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
                Title("See How Your Data is Managed"),
                Container([
                    Label(i)
                    for i in text(r).replace('    ', '').replace('  ', ' ').split('\n\n')
                ]),
                Heading("See? It is safe to use this app!"),
            ], margin=Margin(
                top=Size.pixel(50),
            )),
        ]
    )