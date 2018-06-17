from google.appengine.api import mail

from handlers.base import BaseHandler


class EmailNewCommentWorker(BaseHandler):
    def post(self):
        topic_author_email = self.request.get('topic-author-email')
        topic_title = self.request.get('topic-title')
        topic_id = self.request.get('topic-id')

        mail.send_mail(
            sender="anything@ninja-tech-forum-wd2.appspotmail.com",
            to=topic_author_email,
            subject="New comment on a topic",
            body="""The topic {} received a new comment.

                    Click <a href="https://ninja-tech-forum-wd2.appspot.com/topic/{}/details">on this link</a> to see it
                    """.format(topic_title, topic_id)
        )
