from google.appengine.api import mail

from handlers.base import BaseHandler
from models.forum_subscription import ForumSubscription
from models.topic import Topic


class SendDailyEmail(BaseHandler):
    def get(self):
        forum_subscriptions = ForumSubscription.query().fetch()

        topics = Topic.filter_by_recent_updated().fetch()

        topics_links = ''
        for topic in topics:
            topics_links += '<li><a href="https://ninja-tech-forum-wd2.appspot.com/topic/{}/details">{}</a></li>'.format(
                topic.key.id(), topic.title)

        for subscription in forum_subscriptions:
            mail.send_mail(
                sender="anything@ninja-tech-forum-wd2.appspotmail.com",
                to=subscription.user_email,
                subject="Topics updated in the last 24 hours",
                body="""This is a list of topics updated in the last 24 hours.
                
                <ul>{}</ul>""".format(topics_links)
            )
