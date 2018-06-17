import webapp2

from crons.delete_topics import DeleteTopicsCron
from crons.send_daily_email import SendDailyEmail
from handlers.comment import CommentAddHandler, CommentsFromUserHandler
from handlers.cookie import CookieAlertHandler
from handlers.main import MainHandler, SubscribeHandler
from handlers.topic import TopicAddHandler, TopicDeleteHandler, TopicDetailsHandler, TopicSubscribeHandler
from workers.email_new_comment import EmailNewCommentWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/subscribe', SubscribeHandler, name="subscribe"),
    webapp2.Route('/set-cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/topic/add', TopicAddHandler, name="topic-add"),
    webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetailsHandler, name="topic-details"),
    webapp2.Route('/topic/<topic_id:\d+>/delete', TopicDeleteHandler, name="topic-delete"),
    webapp2.Route('/topic/<topic_id:\d+>/subscribe', TopicSubscribeHandler, name="topic-subscribe"),
    webapp2.Route('/topic/<topic_id:\d+>/add-comment', CommentAddHandler, name="comment-add"),
    webapp2.Route('/my-comments', CommentsFromUserHandler, name="my-comments"),

    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker, name='task-email-new-comment'),

    webapp2.Route('/cron/delete-topics', DeleteTopicsCron, name="cron-delete-topics"),
    webapp2.Route('/cron/send-daily-email', SendDailyEmail, name="send-daily-email"),
], debug=True)
