from handlers.base import BaseHandler
from google.appengine.api import users

from models.comment import Comment
from models.topic import Topic
from utils.decorators import validate_csrf


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

        new_comment = Comment(
            content=comment_content,
            author_email=logged_user.email(),
            topic_id=topic.key.id(),
            topic_title=topic.title,
        )
        new_comment.put()

        return self.redirect_to("topic-details", topic_id=topic.key.id())