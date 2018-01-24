from django.test import TestCase, override_settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from uniqid.testing_utils import MessageTestMixin


class PasswordResetTestCase(MessageTestMixin, TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user("testuser",
                                                         email="test@test.tt",
                                                         password="test")

    def test_existing_email(self):
        url = reverse("users:pwreset")
        response = self.client.post(url,
                                    {'email': self.user.email, 'submit': ''})
        self.assertRedirects(response, reverse("users:emailsent"))
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Password reset')
        # print(mail.outbox[0].body)

    def test_unknown_email(self):
        url = reverse("users:pwreset")
        response = self.client.post(url,
                                    {'email': "bla@bla.bla", 'submit': ''})
        self.assertRedirects(response, reverse("users:emailsent"))
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 0)

    def test_reset(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse("users:setpw", kwargs={"uidb64": uid,
                                             "token": token})
        response = self.client.get(url, follow=True)
        self.assertTrue(response.context_data['validlink'])
        # see PasswordResetConfirmView dispatch method. once the token is
        # stored in the session the url parameter token is set to
        # set-password.
        url = reverse("users:setpw", kwargs={"uidb64": uid,
                                             "token": 'set-password'})
        postresponse = self.client.post(url,
                                        {'new_password1': 'blablabla',
                                         'new_password2': 'blablabla',
                                         'submit': ''}, follow=True)
        self.assertRedirects(postresponse, reverse('users:login'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("blablabla"))
        message = self.getmessage(postresponse)
        self.assertEqual(message.tags, "success")
        self.assertIn("Your password was changed successfully.",
                      message.message)

        url = reverse("users:setpw", kwargs={"uidb64": uid,
                                             "token": token})
        response = self.client.get(url)
        self.assertFalse(response.context_data['validlink'])
