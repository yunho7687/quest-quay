
from flask import render_template, flash, redirect, url_for, current_app, request, jsonify
from flask import g
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Post, Comment
from datetime import datetime, timezone
from app.main.forms import EditProfileForm, EmptyForm, PostForm, SearchForm, CommentForm
from app.main import bp


@bp.before_request
def setTime():
    g.search_form = SearchForm()
    g.post_form = PostForm()
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
        post = Post(title=form.title.data,
                    body=form.post.data, author=current_user)
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

# post detail page


@bp.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    form = CommentForm()
    form_delete_comment = EmptyForm()
    form_like_comment = EmptyForm()
    form_save_comment= EmptyForm()
    form_like_post = EmptyForm()
    form_save_post=EmptyForm()
    form_delete_post=EmptyForm()
    post = db.first_or_404(sa.select(Post).where(Post.id == post_id))
    query = post.comments.select().order_by(Comment.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    comments = db.paginate(query, page=page,
                           per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.explore', page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.explore', page=comments.prev_num) \
        if comments.has_prev else None
    if form.validate_on_submit():
        comment = Comment(body=form.comment.data,
                          post=post, author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment is now live!')
        return redirect(url_for('main.post', post_id=post_id))
    # if form.validate_on_submit():
    return render_template('post_detail.html',  post=post, form=form, comments=comments.items, next_url=next_url, prev_url=prev_url, form_like_comment=form_like_comment, form_like_post=form_like_post,form_save_comment=form_save_comment,form_save_post=form_save_post,form_delete_comment=form_delete_comment,form_delete_post=form_delete_post)


@bp.route('/post/search')
@login_required
def post_search():

    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', '', type=str)
    posts = db.paginate(Post.search_posts(query), page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.post_search', q=g.search_form.q.data, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.post_search', q=g.search_form.q.data, page=posts.prev_num) \
        if posts.has_prev else None
    # return render_template('post_detail.html',  post=post)

    return render_template('post_search.html', query=query, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/post/about_us')
def about_us():
    return render_template('about_us.html')


# @bp.route('/post/<post_id>/popup')
# def test(post_id):
#     return jsonify({'message': 'Hello, World!', 'post_id': post_id})

def handle_comment_action(action_type, comment_id, current_user):
    comment = db.first_or_404(sa.select(Comment).where(Comment.id == comment_id))
    
    if action_type == 'like':
        if current_user.is_liking_comment(comment):
            current_user.unlike_comments(comment)
            db.session.commit()
            return {'success': True, 'action': 'unlike', 'likes': comment.like_count()}
        else:
            current_user.like_comments(comment)
            db.session.commit()
            return {'success': True, 'action': 'like', 'likes': comment.like_count()}
    elif action_type == 'save':
        if current_user.is_saving_comment(comment):
            current_user.unsave_comments(comment)
            db.session.commit()
            return {'success': True, 'action': 'unsave', 'saves': comment.save_count()}
        else:
            current_user.save_comments(comment)
            db.session.commit()
            return {'success': True, 'action': 'save', 'saves': comment.save_count()}
            

@bp.route('/like_comment/<comment_id>', methods=['POST'])
@login_required
def like_comment(comment_id):
    return jsonify(handle_comment_action('like', comment_id, current_user))


@bp.route('/save_comment/<comment_id>', methods=['POST'])
@login_required
def save_comment(comment_id):
    return jsonify(handle_comment_action('save', comment_id, current_user))


@bp.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('main.post', post_id=comment.post_id))

@bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.index'))
    



########################################

    
def handle_post_action(action_type, post_id, current_user):
    post = db.first_or_404(sa.select(Post).where(Post.id == post_id))
    
    if action_type == 'like':
        if current_user.is_liking_post(post):
            current_user.unlike_posts(post)
            db.session.commit()
            likes = post.like_count()
            return {'success': True, 'action': 'unlike', 'likes': likes}
        else:
            current_user.like_posts(post)
            db.session.commit()
            saves = post.like_count()
            return {'success': True, 'action': 'like', 'likes': saves}
    elif action_type == 'save':
        if current_user.is_saving_post(post):
            current_user.unsave_posts(post)
            db.session.commit()
            return {'success': True, 'action': 'unsave', 'saves': post.save_count()}
        else:
            current_user.save_posts(post)
            print(1)
            db.session.commit()
            return {'success': True, 'action': 'save','saves': post.save_count()}
    
    # db.session.commit()
    # return {'success': True, 'action': 'like' if action_type == 'like' else 'save'}

@bp.route('/like_post/<post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    return jsonify(handle_post_action('like', post_id, current_user))



@bp.route('/save_post/<post_id>', methods=['POST'])
@login_required
def save_post(post_id):
    return jsonify(handle_post_action('save', post_id, current_user))
