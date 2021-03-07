from flask import render_template, redirect, url_for,abort,request,flash
from . import main
from flask_login import login_required,current_user
from ..models import User,Blog,Comment,Subscriber
from .form import UpdateProfile,BlogForm,CommentForm
from .. import db,photos
from ..email import mail_message
from ..request import get_quotes

@main.route('/')
def index():
    quotes = get_quotes()
    blogs = Blog.query.all()
    job = Blog.query.filter_by(category = 'Job').all() 
    technology = Blog.query.filter_by(category = 'Technology').all()
    advertisement = Blog.query.filter_by(category = 'Advertisement').all()

    return render_template('index.html', job = job,technology= technology, blogs = blogs,advertisement= advertisement,quote=quotes)

@main.route('/create_new', methods = ['POST','GET'])
@login_required
def new_blog():
    subscribers = Subscriber.query.all()
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user
        new_blog_object = Blog(post=post,user_id=current_user._get_current_object().id,category=category,title=title)
        new_blog_object.save_p()
        for subscriber in subscribers:
            mail_message("New Blog Post","email/new_blog",subscriber.email,new_blog_object=new_blog_object)
        return redirect(url_for('main.index'))
        flash('You Posted a new Blog')

    return render_template('create_blog.html', form = form)

@main.route('/comment/<int:blog_id>', methods = ['POST','GET'])
@login_required
def comment(blog_id):
    form = CommentForm()
    blog = Blog.query.get(blog_id)
    all_comments = Comment.query.filter_by(blog_id = blog_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        blog_id = blog_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,blog_id = blog_id)
        new_comment.save_c()
        return redirect(url_for('.comment', blog_id = blog_id))
    return render_template('comment.html', form =form, blog = blog,all_comments=all_comments)


@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()
    user_id = current_user._get_current_object().id
    posts = Blog.query.filter_by(user_id = user_id).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,posts=posts)

@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_u()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/update.html',form =form)


@main.route('/user/<name>/update/pic',methods= ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',name=name))


@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("Subscribed to D-Blog","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))

@main.route('/blog/<blog_id>/delete', methods = ['POST'])
@login_required
def delete_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("You have deleted your Blog succesfully!")
    return redirect(url_for('main.index'))

