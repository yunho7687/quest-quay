from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
from sqlalchemy import text
import sqlalchemy.orm as so
from flask import current_app

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, db
from hashlib import md5
from time import time
import jwt

# flask db migrate -m "some message" ⬅️ create a migration
# flask db upgrade ⬅️ apply the migration
# flask db downgrade ⬅️ revert the migration

# user_loader is provided by Flask-Login


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


followers = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True)
)

saved_posts = sa.Table(
    'saved_posts',
    db.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey(
        'user.id'), primary_key=True),
    sa.Column('post_id', sa.Integer, sa.ForeignKey(
        'post.id'), primary_key=True)
)


liked_posts = sa.Table(
    'liked_posts',
    db.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey(
        'user.id'), primary_key=True),
    sa.Column('post_id', sa.Integer, sa.ForeignKey(
        'post.id'), primary_key=True)
)


saved_comments = sa.Table(
    'saved_comments',
    db.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey(
        'user.id'), primary_key=True),
    sa.Column('comment_id', sa.Integer, sa.ForeignKey(
        'comment.id'), primary_key=True)
)

liked_comments = sa.Table(
    'liked_comments',
    db.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey(
        'user.id'), primary_key=True),
    sa.Column('comment_id', sa.Integer, sa.ForeignKey(
        'comment.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    avatar_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256),nullable=True)

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')
    # back_populates: reference the name of the relationship attribute on the other side
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    # adding relationship won't lead to database migrations
    comments: so.WriteOnlyMapped['Comment'] = so.relationship(
        back_populates='author')

    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers')
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')

    liked_comments: so.WriteOnlyMapped['Comment'] = so.relationship(
        secondary=liked_comments, primaryjoin=(liked_comments.c.user_id == id),
        secondaryjoin="liked_comments.c.comment_id == comment.c.id",
        back_populates='liked_by')

    saved_comments: so.WriteOnlyMapped['Comment'] = so.relationship(
        secondary=saved_comments, primaryjoin=(saved_comments.c.user_id == id),
        secondaryjoin="saved_comments.c.comment_id == comment.c.id",
        back_populates='saved_by')

    liked_posts: so.WriteOnlyMapped['Post'] = so.relationship(
        secondary=liked_posts, primaryjoin=(liked_posts.c.user_id == id),
        secondaryjoin="liked_posts.c.post_id == post.c.id",
        back_populates='liked_by')

    saved_posts: so.WriteOnlyMapped['Post'] = so.relationship(
        secondary=saved_posts, primaryjoin=(saved_posts.c.user_id == id),
        secondaryjoin="saved_posts.c.post_id == post.c.id",
        back_populates='saved_by')
    
    

    def like_comments(self, comment):
        if not self.is_liking_comment(comment):
            self.liked_comments.add(comment)

    def unlike_comments(self, comment):
        if self.is_liking_comment(comment):
            self.liked_comments.remove(comment)

    def save_comments(self, comment):
        if not self.is_saving_comment(comment):
            self.saved_comments.add(comment)

    def unsave_comments(self, comment):
        if self.is_saving_comment(comment):
            self.saved_comments.remove(comment)

    def like_posts(self, post):
        if not self.is_liking_post(post):
            self.liked_posts.add(post)

    def unlike_posts(self, post):
        if self.is_liking_post(post):
            self.liked_posts.remove(post)

    def save_posts(self, post):
        if not self.is_saving_post(post):
            self.saved_posts.add(post)

    def unsave_posts(self, post):
        if self.is_saving_post(post):
            self.saved_posts.remove(post)

    def is_saving_comment(self, comment):
        query = self.saved_comments.select().where(Comment.id == comment.id)
        return db.session.scalar(query) is not None

    def is_liking_comment(self, comment):
        query = self.liked_comments.select().where(Comment.id == comment.id)
        return db.session.scalar(query) is not None

    def is_liking_post(self, post):
        query = self.liked_posts.select().where(Post.id == post.id)
        return db.session.scalar(query) is not None

    def is_saving_post(self, post):
        query = self.saved_posts.select().where(Post.id == post.id)
        return db.session.scalar(query) is not None

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None

    def followers_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery())
        return db.session.scalar(query)

    def following_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery())
        return db.session.scalar(query)

    def following_posts(self):
        Author = so.aliased(User)
        Follower = so.aliased(User)
        return (
            sa.select(Post)
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(Follower), isouter=True)
            .where(sa.or_(
                Follower.id == self.id,
                # Author.id == self.id,
            ))
            .group_by(Post)
            .order_by(Post.timestamp.desc())
        )

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    title: so.Mapped[str] = so.mapped_column(
        sa.String(50), default='Untitled')

    body: so.Mapped[str] = so.mapped_column(sa.String(500))

    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped['User'] = so.relationship(back_populates='posts')
    # back_populates: reference the name of the relationship attribute on the other side

    comments: so.WriteOnlyMapped['Comment'] = so.relationship(
        back_populates='post',
        passive_deletes='all')
    
    image_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256),nullable=True)


    liked_by: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=liked_posts, primaryjoin=(
            liked_posts.c.post_id == id),
        secondaryjoin=(liked_posts.c.user_id == User.id),
        back_populates='liked_posts',
        passive_deletes='all')

# only wirteonlymapped object have the select method
    saved_by: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=saved_posts, primaryjoin=(
            saved_posts.c.post_id == id),
        secondaryjoin="saved_posts.c.user_id == user.c.id",
        back_populates='saved_posts',
        passive_deletes='all')

    def like_count(self):
        # only wirteonlymapped object have the select method
        query = sa.select(sa.func.count()).select_from(
            self.liked_by.select().subquery())
        return db.session.scalar(query)
    def save_count(self):
    # only wirteonlymapped object have the select method
        query = sa.select(sa.func.count()).select_from(
            self.saved_by.select().subquery())
        return db.session.scalar(query)

        

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    @staticmethod
    def search_posts(query):
        search_query = f'title:{query}* OR body:{query}*'
        # search_query = f'title:{query}* OR body:{query}*'  # search in title and body

        # Direct SQL execution through SQLAlchemy session, now using text() for raw SQL
        sql = text(
            "SELECT post_id FROM post_search WHERE post_search MATCH :query")

        result = db.session.execute(sql, {'query': search_query})

        post_ids = [row[0] for row in result.fetchall()]
        # row is a tuple, rowp[0] is the first element of the tuple

        # a list of Post objects
        return Post.query.filter(Post.id.in_(post_ids)).order_by(Post.timestamp.desc())


class Comment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Post.id))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))

    post: so.Mapped[Post] = so.relationship(back_populates='comments')

    author: so.Mapped[User] = so.relationship(back_populates='comments')
    
    image_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256),nullable=True)

    liked_by: so.WriteOnlyMapped[User] = so.relationship(
        secondary=liked_comments, primaryjoin=(
            liked_comments.c.comment_id == id),
        secondaryjoin="liked_comments.c.user_id == user.c.id",
        back_populates='liked_comments',
        passive_deletes='all' )

    saved_by: so.WriteOnlyMapped[User] = so.relationship(
        secondary=saved_comments, primaryjoin=(
            saved_comments.c.comment_id == id),
        secondaryjoin="saved_comments.c.user_id == user.c.id",
        back_populates='saved_comments',passive_deletes='all')

    def like_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.liked_by.select().subquery())
        return db.session.scalar(query)
    def save_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.saved_by.select().subquery())
        return db.session.scalar(query)
