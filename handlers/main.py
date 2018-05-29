from handlers.base import BaseHandler
from models.topic import Topic


class MainHandler(BaseHandler):
    def get(self):
        topics = Topic.query(Topic.deleted == False).fetch()

        context = {
            "topics": topics,
        }

        return self.render_template("main.html", params=context)