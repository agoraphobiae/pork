# what each page will look like

from app import app
from flask import render_template, flash, redirect
# from forms import LoginForm

from game import ham


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
            'body':'this a test',
            'body':'this is where the game output goes.'
        }]

    ham.ham()

    return render_template("game.html",
        user = user,
        msgs = msgs)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     loginform = LoginForm()
#     if loginform.validate_on_submit():
#         flash('Login requested for OpenID="' + loginform.openid.data + '", remember_me=' + str(loginform.remember_me.data))
#         return redirect('/index')

#     return render_template("login.html",
#         title="Log in", form=loginform,
#         providers = app.config['OPENID_PROVIDERS'])
