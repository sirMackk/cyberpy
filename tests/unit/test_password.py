import unittest as t

from secrettunnel.passwords import SimpleNumericPassword
from secrettunnel.exceptions import OnetimePasswordError


class TestSimpleNumericPassword(t.TestCase):
    def setUp(self):
        self.password_container = SimpleNumericPassword()

    def test_generate_password_in_range(self):
        self.password_container.generate(1)
        self.assertIn(int(self.password_container.password), range(0, 10))

    def test_cannot_generate_more_than_one_passwords(self):
        self.password_container.generate()

        with self.assertRaisesRegex(OnetimePasswordError,
                                    'already generated'):
            self.password_container.generate()

    def test_validates_password(self):
        password = self.password_container.generate()

        self.assertFalse(self.password_container.validate('nope'))
        self.assertTrue(self.password_container.validate(password))
