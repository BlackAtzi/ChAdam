from flask import render_template, flash, redirect, url_for
from app import app, db, lm
from .forms import LoginForm, PostForm, CreateForumForm, ImgForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from .models import User, Forum, Post
import datetime
import pytz


def utc_to_local():
    local_dt = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Europe/Copenhagen"))
    return pytz.timezone("Europe/Copenhagen").normalize(local_dt)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@lm.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/', methods=['GET', 'POST'])
def root_page():
    form = LoginForm()
    existingUser = False
    if current_user.is_authenticated():
        return redirect('/index')
    if form.validate_on_submit():
        users = User.query.all()
        for u in users:
            if u.nickname.lower() == form.username.data.lower():
                existingUser = True
                myUser = u

        if existingUser:
            if myUser.password == form.password.data:
                login_user(myUser)
                return redirect("/index")
            else:
                flash("Incorrect password.")
                return redirect("/")
        else:
            flash("The user {} doesn't exist yet.".format(form.username.data))
            return redirect("/")
    return render_template("root_page.html",
                          form=form)

@app.route('/newuser', methods=['GET', 'POST'])
def new_user():
    form = LoginForm()
    taken = False
    if form.validate_on_submit():
        users = User.query.all()
        for u in users:
            if u.nickname.lower() == form.username.data.lower():
                taken = True
        if taken:
            flash("Username already taken")
            return redirect('/newuser')
        else:
            newUser = User(nickname=form.username.data, password=form.password.data)
            db.session.add(newUser)
            db.session.commit()
            flash("User {} created successfully.".format(form.username.data))
            return redirect('/')
    return render_template("new_user.html",
                           form=form)

@app.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    form = CreateForumForm()
    taken = False
    if form.validate_on_submit():
        forums = Forum.query.all()
        for myForum in forums:
            if myForum.name.lower() == form.forum_name.data.lower():
                taken = True
        if taken:
            flash("A forum with that name, already exists.")
            return redirect('/index/')
        else:
            newForum = Forum(name=form.forum_name.data)
            db.session.add(newForum)
            db.session.commit()
            flash("Forum {} created successfully.".format(form.forum_name.data))
            return redirect('/')
    return render_template("index.html", forums=Forum.query.all(), form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/index/<forum_id>', methods=['GET', 'POST'])
@login_required
def show_forum(forum_id):
    postform = PostForm()
    imgform = ImgForm()
    if postform.validate_on_submit():
        newPost = Post(body=postform.post.data, timestamp=str(utc_to_local())[0:-16], user_id=current_user.get_id(), forum_id=forum_id, is_img=False)
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for('show_forum', forum_id=forum_id))
    elif imgform.validate_on_submit():
        imgPostBody = '<img src="{}" />'.format(imgform.postImg.data)
        newPost = Post(body=imgPostBody, timestamp=str(utc_to_local())[0:-16], user_id=current_user.get_id(), forum_id=forum_id, is_img=True)
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for('show_forum', forum_id=forum_id))
    return render_template("forum.html",
                           posts=Forum.query.get(forum_id).posts.all(),
                           users=User.query.all(),
                           forum=Forum.query.get(forum_id),
                           postform=postform,
                           imgform=imgform
    )