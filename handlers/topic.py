import uuid

from handlers.base import BaseHandler
from google.appengine.api import memcache, users

from models.comment import Comment
from models.topic import Topic
from utils.decorators import validate_csrf


class TopicAddHandler(BaseHandler):
    def get(self):
        return self.render_template("topic_add.html", generate_csrf_token=True)

    @validate_csrf
    def post(self):
        title = self.request.get("title")
        text = self.request.get("text")

        if not title:
            return self.write("Title field is required")

        if not text:
            return self.write("Text field is required")

        logged_user = users.get_current_user()

        new_topic = Topic.create(
            title=title,
            content=text,
            user=logged_user,
        )

        return self.redirect_to("topic-details", topic_id=new_topic.key.id())


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query(Comment.deleted == False).filter(Comment.topic_id == int(topic_id)).order(
            Comment.created).fetch()

        context = {
            "topic": topic,
            "comments": comments,
        }

        return self.render_template("topic_details.html", params=context, generate_csrf_token=True)
