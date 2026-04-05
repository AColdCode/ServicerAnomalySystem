import re


class RegularMatch:
    def __init__(self):
        self.usernameMatch = r'^[A-Za-z0-9_]{1,20}$'
        self.passwordMatch = r'^\S{6,}$'

    def isLegalUsername(self, username):
        return bool(re.fullmatch(self.usernameMatch, username))

    def isLegalPassword(self, password):
        return bool(re.fullmatch(self.passwordMatch, password))
