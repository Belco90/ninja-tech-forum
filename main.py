import webapp2

from handlers.cookie import CookieAlertHandler
from handlers.main import MainHandler
from handlers.topic import TopicAddHandler, TopicDetailsHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/topic/add', TopicAddHandler, name="topic-add"),
    webapp2.Route('/topic/details/<topic_id:\d+>', TopicDetailsHandler, name="topic-details"),
], debug=True)
