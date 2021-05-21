class LoginError(Exception):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return f'{self.username} {self.password} is wrong'

class TooManyReqError(Exception):
    def __str__(self):
        return 'You have sent too many requests'
