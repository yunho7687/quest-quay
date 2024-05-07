
from flask import render_template, flash, redirect, url_for, current_app, request, jsonify
from flask import g
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Post
from datetime import datetime, timezone
from app.main.forms import EditProfileForm, EmptyForm, PostForm, SearchForm
from app.main import bp
from urllib.parse import unquote


@bp.before_request
def setTime():
    g.search_form = SearchForm(request.args)
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
        


@bp.route('/', methods=['GET', 'POST'])
def intro():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('intro.html')


@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    if current_user.is_anonymous:
        posts = db.paginate(Post.query.order_by(Post.timestamp.desc()), page=page,
                            per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    else:
        # posts = db.session.scalars(current_user.following_posts()).all()
        posts = db.paginate(current_user.following_posts(), page=page,
                            per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    # posts = db.session.scalars(query).all()
    posts = db.paginate(query, page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template("index.html", title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/user/')
@bp.route('/user/<username>')
@login_required
def user(username):

    user = db.first_or_404(sa.select(User).where(User.username == username))
    page = request.args.get('page', 1, type=int)
    # query = sa.select(Post).join(Post.author).where(
    #     User.username == username).order_by(Post.timestamp.desc())
    query = user.posts.select().order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'],
                        error_out=False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None

    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    form = EmptyForm()
    return render_template('user_popup.html', user=user, form=form)


@bp.route('/test')
def test():
    return jsonify({'message': 'Hello, World!'})


@bp.route('/post/<post_id>', methods=['GET'])
def post(post_id):
    post = db.first_or_404(sa.select(Post).where(Post.id == post_id))
    return render_template('post_detail.html',  post=post)


@bp.route('/post/search')
@login_required
def post_search():
    if not g.search_form.validate():
        print(g.search_form.errors)
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', '', type=str)
    posts = db.paginate(Post.search_posts(query), page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.post_search',q=g.search_form.q.data, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.post_search',q=g.search_form.q.data, page=posts.prev_num) \
        if posts.has_prev else None
    # return render_template('post_detail.html',  post=post)

    return render_template('post_search.html', query=query, posts=posts.items, next_url=next_url, prev_url=prev_url)

# @bp.route('/post/<post_id>/popup')
# def test(post_id):
#     return jsonify({'message': 'Hello, World!', 'post_id': post_id})
