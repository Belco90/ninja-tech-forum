import os
import unittest
import webapp2
import webtest

from google.appengine.ext import testbed
from google.appengine.api import memcache
from handlers.topic import TopicAddHandler, TopicDetailsHandler
from models.topic import Topic


class TopicTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/topic/add', TopicAddHandler, name="topic-add"),
                webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetailsHandler, name="topic-details"),
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        # self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_topic_add_handler(self):
        # GET
        response = self.testapp.get('/topic/add')
        self.assertEqual(response.status_int, 200)

    def test_get_topic_add_handler_user_not_logged(self):
        # arrange
        os.environ['USER_EMAIL'] = ''

        # act
        response = self.testapp.post('/topic/add')

        # assert
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, "Please login before you're allowed to go ahead")

    def test_post_topic_add_handler(self):
        # Arrange
        csrf_token = "123abc"
        memcache.add(key=csrf_token, value='some.user@example.com', time=600)

        request_args = {
            "title": "test title",
            "text": "test text",
            "csrf-token": csrf_token,
        }

        # Act
        response = self.testapp.post('/topic/add', request_args)

        # Assert
        self.assertEqual(response.status_int, 302, response.body)

        topic = Topic.query().get()
        self.assertEqual(topic.title, request_args["title"])
        self.assertEqual(topic.content, request_args["text"])
