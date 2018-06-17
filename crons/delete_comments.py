from datetime import datetime, timedelta

from handlers.base import BaseHandler
from models.comment import Comment


class DeleteCommentsCron(BaseHandler):
    def get(self):
        deleted_comments = Comment.query(Comment.deleted == True)

        overdue_comments = deleted_comments.filter(Comment.updated < (datetime.now() - timedelta(days=30)))

        comments_to_be_removed = overdue_comments.fetch()

        for comment in comments_to_be_removed:
            comment.key.delete()
