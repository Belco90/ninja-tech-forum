from google.appengine.ext import ndb


class ForumSubscription(ndb.Model):
    user_email = ndb.StringProperty()

    @classmethod
    def create(cls, user):
        new_subscription = cls(
            user_email=user.email(),
        )
        new_subscription.put()

        return new_subscription