from handlers.base import BaseHandler
from models.topic import Topic
from utils.decorators import validate_csrf


class MainHandler(BaseHandler):
    def get(self):
        topics = Topic.query(Topic.deleted == False).fetch()

        context = {
            "topics": topics,
        }

        return self.render_template("main.html", params=context)
