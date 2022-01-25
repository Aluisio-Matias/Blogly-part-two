"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'keep_it_a_secret'
app.debug = False
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


############ Start with a list of Posts ###############################

@app.route('/')
def root():
    '''display recent list of posts'''
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts/home.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    '''Show 404 page not found'''
    return render_template('404.html'), 404


############ Users Route ##############################################

@app.route('/users')
def user_listing():
    '''Display list of all Users in db'''
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new_user', methods=["GET"])
def new_user_form():
    '''Display the form to create a new user'''
    return render_template('users/new_user.html')

@app.route('/users/new_user', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()
    flash(f'User {new_user.full_name} has been added.')

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    '''Display specific users info'''
    user = User.query.get_or_404(user_id)
    return render_template('users/show_user.html', user=user)

@app.route('/users/<int:user_id>/edit_user')
def edit_user(user_id):
    '''Display a form to edit an existing user'''
    user = User.query.get_or_404(user_id)
    return render_template('users/edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit_user', methods=["POST"])
def update_user(user_id):
    '''handle form for updating user'''

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f'User {user.full_name} edited.')

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    '''handle form submission to delete user'''

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.full_name} deleted.')

    return redirect('/users')


################ Posts Route #############################################

@app.route('/users/<int:user_id>/posts/new_post')
def posts_new_form(user_id):
    '''display the form to create a new post for a specific user'''

    user = User.query.get_or_404(user_id)
    return render_template('posts/new_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new_post', methods=["POST"])
def new_posts(user_id):
    '''handle the form submission for creating a new post for the user'''

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f'Post "{new_post.title}" added.')

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    '''show a page with information of a specific post'''

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit_post')
def edit_post(post_id):
    '''show form to edit an existing post'''

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit_post', methods=['POST'])
def update_post(post_id):
    '''Handle form submission for updating an existing post'''

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f'Post "{post.title}" edited.')

    return redirect(f'/users/{post.user_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    ''' handle form submission for deleting an existing post '''

    post = Post.query.get_or_404(post_id)

    db.session.add(post)
    db.session.commit()
    flash(f'Post "{post.title}" has been deleted!')

    return redirect(f'/users/{post.user_id}')






