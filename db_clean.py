from app import db, models

forums = models.User.query.all()
for forum in forums:
    db.session.delete(forum)

posts = models.Post.query.all()
for post in posts:
    db.session.delete(post)

users = models.User.query.all()
for user in users:
    db.session.delete(user)

db.session.commit()

