from random import randint

from cyberpy.exceptions import OnetimePasswordError


class AbstractOnetimePassword:
    def generate_password(self, *args, **kwargs):
        raise NotImplementedError()

    def validate_password(self, password):
        raise NotImplementedError()


class SimpleNumericPassword(AbstractOnetimePassword):
    def __init__(self):
        self.password = None

    def generate(self, length=4):
        if self.password is not None:
            raise OnetimePasswordError('Password already generated')

        min_range = 10 ** (length - 1)
        max_range = (10 ** length) - 1
        self.password = str(randint(min_range, max_range))
        return self.password

    def validate(self, password):
        return self.password == password
