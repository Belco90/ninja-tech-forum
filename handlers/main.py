from google.appengine.api import users

from handlers.base import BaseHandler
from models.topic import Topic
from models.forum_subscription import ForumSubscription
from utils.decorators import validate_csrf


class MainHandler(BaseHandler):
    def get(self):
        topics = Topic.query(Topic.deleted == False).fetch()

        show_subscribe_button = False
        logged_user = users.get_current_user()

        if logged_user:
            show_subscribe_button = ForumSubscription.query(
                ForumSubscription.user_email == logged_user.email()).count() == 0

        context = {
            "topics": topics,
            "show_subscribe_button": show_subscribe_button
        }

        return self.render_template("main.html", params=context, generate_csrf_token=True)


class SubscribeHandler(BaseHandler):

    @validate_csrf
    def post(self):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to subscribe.")

        ForumSubscription.create(user=logged_user)

        return self.redirect_to("main-page")
