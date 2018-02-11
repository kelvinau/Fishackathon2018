TOKEN_KEY_NAME = 'token'
USER_ID_KEY_NAME = 'user_id'


class UserSessionMixin(object):
    def log_in(self, user_id, token):
        self.session[USER_ID_KEY_NAME] = user_id
        self.session[TOKEN_KEY_NAME] = token

    def get_user_token(self):
        return self.session.get(TOKEN_KEY_NAME)

    def get_user_id(self):
        return self.session.get(USER_ID_KEY_NAME)

    def log_out(self):
        if USER_ID_KEY_NAME in self.session:
            self.session.pop(USER_ID_KEY_NAME)
        if TOKEN_KEY_NAME in self.session:
            self.session.pop(TOKEN_KEY_NAME)
