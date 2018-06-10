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
        new_topic_subscription.put()

        return new_topic_subscription

    @classmethod
    def is_user_subscribed(cls, user, topic):
        subscription_length = cls.query(cls.topic_id == topic.key.id()).filter(cls.user_email == user.email()).count()

        return subscription_length > 0
