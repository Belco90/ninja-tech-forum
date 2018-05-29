import webapp2

from handlers.cookie import CookieAlertHandler
from handlers.main import MainHandler
from handlers.topic import TopicAdd, TopicDetails

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/topic/add', TopicAdd, name="topic-add"),
    webapp2.Route('/topic/details/<topic_id:\d+>', TopicDetails, name="topic-details"),
], debug=True)
