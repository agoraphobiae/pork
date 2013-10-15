# what each page will look like

from app import app
from flask import render_template, flash, redirect, session, request, url_for, escape
# from forms import LoginForm

from game import ham

# want saves to persist
session.permanent = True
app.permanent_session_lifetime = timedelta(365)
# erm i guess we're using flask-login now

@app.route('/')
@app.route('/index')
def index():
    #placeholder vars
    user = {'nickname': 'Pork flask'}
    posts = [
        {
            'author': {'nickname': 'Miguel'},
            'body': 'Sometime I should change this.'
        },
        {
            'author': {'nickname': 'Wilshire'},
            'body': 'Should I buy a new guitar?'
        }
    ]
    
    return render_template("index.html",
        title="Home",
        user = user,
        posts = posts)

@app.route('/play')
def play():
    if 'username' in session:
        user = {'nickname': escape(session['username'])}
    else:
        user = {'nickname': 'agoraphobiae'}

    msgs = [
        {
            'body':'this a test'
        },
        {
            'body':'this is where the game output goes.'
        }]

    return render_template("game.html",
        user = user,
        msgs = msgs)

@app.route('/play/<command>')
def playcmd(command):
    # dummy vars
    user = {'nickname': 'agoraphobiae'}
    msgs = [
        {
            'body':command,
            'body':'this is where the game output goes.'
        }]

    ham.ham()

    return render_template("game.html",
        user = user,
        msgs = msgs)


# session management for gameplay
@app.route('/login', methods=['GET', 'POST'])
def login():
    # goddammit dummy vars
    user = {'nickname': 'agoraphobiae'}
    msgs = [
        {
            'body':'command',
            'body':'this is where the game output goes.'
        }]
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template("game.html",
        user = user,
        msgs = msgs,
        login = True)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# random shit please change
# ty wordpress
app.secret_key = "v.]0SM8_i/66]=[jszHs0?Nc+#CpK,L{heEPfMouTJam<{e_>pR>]baad*,Wz{om"

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     loginform = LoginForm()
#     if loginform.validate_on_submit():
#         flash('Login requested for OpenID="' + loginform.openid.data + '", remember_me=' + str(loginform.remember_me.data))
#         return redirect('/index')

#     return render_template("login.html",
#         title="Log in", form=loginform,
#         providers = app.config['OPENID_PROVIDERS'])
