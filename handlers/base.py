#!/usr/bin/env python
import os
import uuid
import json

import jinja2
import webapp2
from google.appengine.api import memcache, users


template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None, generate_csrf_token=False):
        if not params:
            params = {}

        # cookie
        cookie_law = self.request.cookies.get("cookie_law")
        if cookie_law:
            params["cookies"] = True

        # google login
        logged_user = users.get_current_user()
        if logged_user:
            params["user"] = logged_user
            params["logout_url"] = users.create_logout_url('/')

            # generate csrf token only if asked and user logged (we need their email)
            if generate_csrf_token:
                csrf_token = str(uuid.uuid4())
                memcache.add(key=csrf_token, value=logged_user.email(), time=600)
                params["csrf_token"] = csrf_token

        else:
            params["login_url"] = users.create_login_url('/')


        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

    def render_json(self, params=None):
        if not params:
            params = {}

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(params))
