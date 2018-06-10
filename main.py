import webapp2

from handlers.comment import CommentAddHandler
from handlers.cookie import CookieAlertHandler
from handlers.main import MainHandler
from handlers.topic import TopicAddHandler, TopicDeleteHandler, TopicDetailsHandler
from workers.email_new_comment import EmailNewCommentWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/topic/add', TopicAddHandler, name="topic-add"),
    webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetailsHandler, name="topic-details"),
    webapp2.Route('/topic/<topic_id:\d+>/delete', TopicDeleteHandler, name="topic-delete"),
    webapp2.Route('/topic/<topic_id:\d+>/add-comment', CommentAddHandler, name="comment-add"),
    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker, name='task-email-new-comment'),
], debug=True)
