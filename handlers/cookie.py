from handlers.base import BaseHandler


class CookieAlertHandler(BaseHandler):
    def post(self):
        self.response.set_cookie(key="cookie_law", value="accepted")

        context = {
            "accepted": True,
        }

        return self.render_json(context)
