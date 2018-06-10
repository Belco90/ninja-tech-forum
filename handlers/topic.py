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


class TopicDeleteHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        context = {
            "topic": topic,
        }

        return self.render_template("topic_delete.html", params=context, generate_csrf_token=True)

    @validate_csrf
    def post(self, topic_id):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to delete a topic.")

        topic = Topic.get_by_id(int(topic_id))

        is_admin = users.is_current_user_admin()
        is_author = topic.author_email == logged_user.email()

        if not is_admin and not is_author:
            return self.write("Only topic author or admin user can delete a Topic")

        topic.delete()

        comments = Comment.filter_by_topic(int(topic_id)).fetch()

        for comment in comments:
            comment.delete()

        return self.redirect_to("main-page")


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.filter_by_topic(int(topic_id)).order(Comment.created).fetch()

        logged_user = users.get_current_user()

        context = {
            "topic": topic,
            "comments": comments,
            "can_delete": users.is_current_user_admin() or (logged_user and topic.author_email == logged_user.email()),
        }

        return self.render_template("topic_details.html", params=context, generate_csrf_token=True)
