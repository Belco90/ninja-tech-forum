import webapp2

from handlers.cookie import CookieAlertHandler
from handlers.main import MainHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieAlertHandler, name="set-cookie")
], debug=True)
