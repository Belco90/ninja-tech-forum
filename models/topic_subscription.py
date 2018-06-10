from google.appengine.ext import ndb


class TopicSubscription(ndb.Model):
    user_email = ndb.StringProperty()
    topic_id = ndb.IntegerProperty()

    @classmethod
    def create(cls, user, topic):
        new_topic_subscription = cls(
            user_email=user.email(),
            topic_id=topic.key.id()
        )
