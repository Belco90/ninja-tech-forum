from handlers.base import BaseHandler
from google.appengine.api import users

from models.topic import Topic


class TopicAdd(BaseHandler):
    def get(self):
        return self.render_template("topic_add.html")

    def post(self):
        user = users.get_current_user()

        if not user:
            return self.write("Please login before you're allowed to post a topic.")

        title = self.request.get("title")
        text = self.request.get("text")

        if not title:
            return self.write("Title field is required")

        if not text:
            return self.write("Text field is required")

        new_topic = Topic(title=title, content=text, author_email=user.email())
        new_topic.put()

        return self.write("Topic successfully created!")
