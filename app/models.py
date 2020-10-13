from . import db, ma
from datetime import datetime
import enum
from cloudinary.models import CloudinaryField

class MediaList(enum.Enum):
    '''
    Model choices for the media types
    '''
    photo = "photo"
    video = "video"
    audio = "audio"

class CategoryList(enum.Enum):
    '''
    Model Choices for the Post Categories
    '''
    africanhistory = "africanhistory"
    contemporaryafrican = "contemporaryafrican"
    neoafrican = "neoafrican"

class LicensingList(enum.Enum):
    '''
    Model choices for the post licensing
    '''
    creativecommons = "creativecommons"

# Association Table for a Profile and its followers
followers = db.Table('followers',
    db.Column('follower_id', db.integer, db.ForeignKey('profiles.id')),
    db.Column('followed_id', db.integer, db.ForeignKey('profiles.id'))
)

class Profile(db.Model):
    '''
    Database model for profiles
    '''
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    country = db.Column(db.String(255), nullable=False)
    facebook = db.Column(db.String(255), nullable=True)
    twitter = db.Column(db.String(255), nullable=True)
    google = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    remember_token = db.Column(db.Boolean, default=False, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    posts = db.relationship('Post', backref='post_profile', lazy='dynamic')
    liker = db.relationship('Like', backref='liked_profile', lazy='dynamic')
    followed = db.relationship('Profile', secondary=followers, primaryjoin=(followers.c.follower_id == id), secondaryjoin=(followers.c.followed_id == id), db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, profile):
        if not self.is_following(profile):
            self.followed.append(profile)
    
    def unfollow(self, profile):
        if self.is_following(profile):
            self.followed.remove(profile)

    def is_following(self, profile):
        return self.followed.filter(
            followers.c.followed_id == profile.id
        ).count() > 0

    def like_post(self, post):
        if not self.has_liked(post):
            like = Like(profile_id=self.id, post_id=post.id)
            db.session.add(like)
            db.session.commit()
    
    def unlike_post(self, post):
        if self.has_liked(post):
            Like.query.filter_by(profile_id=self.id, post_id=post.id).delete()
            db.session.commit()
    
    def has_liked(self, post):
        return Like.query.filter(
            Like.profile_id == self.id,
            Like.post_id == post.id
        ).count() > 0
    
    def my_posts(self):
        return Post.query.filter_by(profile_id == self.id).order_by(Post.timestamp.desc())

    def timeline(self):
        ''' My posts and others based on timestamps'''
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.profile_id).filter(
                followers.c.follower_id == self.id
            )
        )
        own = Post.query.filter_by(profile_id == self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def save_profile(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_profile(self):
        db.session.delete(self)
        db.session.commit()

    def reactivate_profile(self):
        self.is_active = True
        db.session.add(self)
        db.session.commit()
    
    def deactivate_profile():
        self.is_active = False
        db.session.add(self)
        db.session.commit()
    
    def verify_profile():
        self.is_verified = True
        db.session.add(self)
        db.session.commit()

    def deverify_profile(self):
        self.is_verified = False
        db.session.add(self)
        db.session.commit()


# Association Table for posts and tags
tags = db.Table('tags', 
    db.Column('tag_id', db.Integer, db.ForeignKey('posttags.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)

class Post(db.Model):
    '''
    Database model for posts
    '''
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    media = CloudinaryField('image')
    post_name = db.Column(db.String(255), unique=True, nullable=False)
    post_type = db.Column(db.String(255), default=MediaList.photo, nullable=False)
    post_location = db.Column(db.String(255), nullable=False)
    post_category = db.Column(db.String(255), default=CategoryList.africanhistory, nullable=False)
    post_licensing = db.Column(db.String(255), default=LicensingList.creativecommons, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    comments = db.relationship('Comment', backref='comment_post', lazy='dynamic')
    liked = db.relationship('Like', backref='liked_post', lazy='dynamic')
    tags = db.relationship('PostTag', secondary=tags, lazy='subquery', backref=db.backref('tagged_post', lazy=True))

    def save_post(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

    def search_by_post_name(self, search_text):
        return Post.query.filter_by(post_name == search_text).all()
    
    def search_by_post_type(self, search_text):
        return Post.query.filter_by(post_type == search_text).all()

    def search_by_post_category(self, search_text):
        return Post.query.filter_by(post_category == search_text).all()

    def search_by_post_location(self, search_text):
        return Post.query.filter_by(post_location == search_text).all()

    def search_by_post_licensing(self, search_text):
        return Post.query.filter_by(post_licensing == search_text).all()
    
    def add_post_tag(self, tag):
        if not self.has_tag(tag):
            self.tags.append(tag)
    
    def remove_post_tag(self, tag):
        if self.has_tag(tag):
            self.tags.remove(tag)
    
    def has_tag(self, tag):
        return PostTag.query.filter(
            PostTag.id == tag.id
        )
        

class PostTag(db.Model):
    '''
    Database model for tags belonging to posts
    '''
    __tablename__ = 'posttags'

    id = db.Column(db.Integer, primary_key=True)
    tag_text = db.Column(db.String(255), nullable=False)

    def save_tag(self):
        db.session.add(self)
        db.session.commit()

    def delete_tag(self):
        db.session.delete(self)
        db.session.commit()

class Comment(db.Model):
    '''
    Database model for comments
    '''
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

class Like(db.Model):
    '''
    Database model for likes
    '''
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))