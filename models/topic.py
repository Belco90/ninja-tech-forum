from datetime import datetime, timedelta

from google.appengine.ext import ndb


class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, title, content, user):
        new_topic = cls(
            title=title,
            content=content,
            author_email=user.email(),
        )
        new_topic.put()

        return new_topic

    def delete(self):
        self.deleted = True
        self.put()

        return self

    @classmethod
    def filter_by_recent_updated(cls):
        topics = cls.query(cls.deleted == False)
        topics = topics.filter(cls.updated > (datetime.now() - timedelta(hours=24)))

        return topics
