import uuid

from handlers.base import BaseHandler
from google.appengine.api import memcache, users

from models.topic import Topic


class TopicAddHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if not user:
            return self.write("Please login before you're allowed to post a topic.")

        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value=user.email(), time=600)

        context = {
            "csrf_token": csrf_token,
        }

        return self.render_template("topic_add.html", params=context)

    def post(self):
        user = users.get_current_user()

        if not user:
            return self.write("Please login before you're allowed to post a topic.")

        csrf_token = self.request.get("csrf_token")
        mem_token = memcache.get(key=csrf_token)

        if not mem_token or mem_token != user.email():
            return self.write("CSRF Token is protecting this website :)")

        title = self.request.get("title")
        text = self.request.get("text")

        if not title:
            return self.write("Title field is required")

        if not text:
            return self.write("Text field is required")

        new_topic = Topic(title=title, content=text, author_email=user.email())
        new_topic.put()

        return self.redirect_to("topic-details", topic_id=new_topic.key.id())


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        context = {
            "topic": topic,
        }

        return self.render_template("topic_details.html", params=context)
