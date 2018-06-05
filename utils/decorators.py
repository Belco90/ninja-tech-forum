from google.appengine.api import memcache, users


def validate_csrf(handler):
    def wrapper(self, *args, **kwargs):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to go ahead")

        csrf_token = self.request.get("csrf-token")
        mem_token = memcache.get(key=csrf_token)

        if not mem_token or mem_token != logged_user.email():
            return self.write("CSRF Token is protecting this website :)")

        return handler(self, *args, **kwargs)

    return wrapper
