from google.appengine.ext import ndb
from google.appengine.api import taskqueue

from models.topic_subscription import TopicSubscription


class Comment(ndb.Model):
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    topic_id = ndb.IntegerProperty()
    topic_title = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, content, user, topic):
        new_comment = cls(
            content=content,
            author_email=user.email(),
            topic_id=topic.key.id(),
            topic_title=topic.title,
        )
        new_comment.put()

        subscriptions = TopicSubscription.query(TopicSubscription.topic_id == topic.key.id()).fetch()

        subscribers = [topic.author_email, ]
        for subscription in subscriptions:
            if subscription.user_email != user.email():
                subscribers.append(subscription.user_email)

        # send notification to topic author and subscribers
        for email in subscribers:
            taskqueue.add(
                url='/task/email-new-comment',
                params={
                    'topic-author-email': email,
                    'topic-title': topic.title,
                    'topic-id': topic.key.id(),
                }
            )

        return new_comment

    def delete(self):
        self.deleted = True
        self.put()

        return self

    @classmethod
    def filter_by_topic(cls, topic_id):
        return cls.query(cls.deleted == False).filter(cls.topic_id == topic_id)

    @classmethod
    def filter_by_user(cls, user_email):
        return cls.query(cls.deleted == False).filter(cls.author_email == user_email)
