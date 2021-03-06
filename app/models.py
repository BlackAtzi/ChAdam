from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    posts = db.relationship('Post', backref='forum', lazy='dynamic')

    def __repr__(self):
        return '<Forum %r>' % (self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(500))
    timestamp = db.Column(db.String)
    is_img = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)