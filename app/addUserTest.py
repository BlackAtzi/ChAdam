from app import db, models
import datetime

#f = models.Forum(name="Test")
#db.session.add(f)
#db.session.commit()

#print(models.Forum.query.all())
forums = models.Forum.query.all()
print(forums)
db.session.commit()

