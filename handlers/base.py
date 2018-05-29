#!/usr/bin/env python
import os
import jinja2
import webapp2
from google.appengine.api import users


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

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}

        # cookie
        cookie_law = self.request.cookies.get("cookie_law")
        if cookie_law:
            params["cookies"] = True

        # google login
        user = users.get_current_user()
        if user:
            params["user"] = user
            params["logout_url"] = users.create_logout_url('/')
        else:
            params["login_url"] = users.create_login_url('/')

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))