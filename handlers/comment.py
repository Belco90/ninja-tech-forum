from handlers.base import BaseHandler
from google.appengine.api import users

from models.comment import Comment
from models.topic import Topic
from utils.decorators import validate_csrf


class CommentsFromUserHandler(BaseHandler):
    def get(self):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to see your comments.")

        comments = Comment.filter_by_user(logged_user.email()).fetch()

        context = {
            "comments": comments,
        }

        return self.render_template("comments.html", params=context)


class CommentAddHandler(BaseHandler):

    @validate_csrf
    def post(self, topic_id):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to add a comment.")

        comment_content = self.request.get('comment-content')

        if not comment_content:
            return self.write("Comment content field is required")

        topic = Topic.get_by_id(int(topic_id))

        Comment.create(
            content=comment_content,
            user=logged_user,
            topic=topic,
        )

        return self.redirect_to("topic-details", topic_id=topic.key.id())


class CommentDeleteHandler(BaseHandler):
    def get(self, comment_id):
        comment = Comment.get_by_id(int(comment_id))
        topic = Topic.get_by_id(comment.topic_id)

        context = {
            "comment": comment,
            "topic": topic,
        }

        return self.render_template("comment_delete.html", params=context, generate_csrf_token=True)

    @validate_csrf
    def post(self, comment_id):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to delete a comment.")

        comment = Comment.get_by_id(int(comment_id))
        topic = Topic.get_by_id(comment.topic_id)

        if logged_user.email() != comment.author_email:
            return self.write("Only comment author can delete a Comment")

        comment.delete()

        return self.redirect_to("topic-details", topic_id=topic.key.id())
