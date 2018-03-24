from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from uniqid.testing_utils import MessageTestMixin
from ..forms import default_token_generator
from pages.models import Page

UserModel = get_user_model()


class PasswordResetTestCase(MessageTestMixin, TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user("testuser",
                                                  email="test@test.tt",
                                                  password="test")
        self.user.profile.email_confirmed = True
        self.user.profile.save()

    def test_existing_email(self):
        url = reverse("users:resetpw")
        response = self.client.post(url,
                                    {'email': self.user.email, 'submit': ''})
        self.assertRedirects(response, reverse("users:emailsent"))
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Password reset')
        # print(mail.outbox[0].body)

    def test_unknown_email(self):
        url = reverse("users:resetpw")
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


class RegistrationTestCase(MessageTestMixin, TestCase):
    def test_new_email(self):
        url = reverse("users:register")
        response = self.client.post(url,
                                    {'email': "bla@bla.bla"}, follow=True)
        self.assertRedirects(response, reverse("pages:createpage"))
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject,
                         'Finalize your registration')
        user = UserModel.objects.get(username="bla@bla.bla")
        self.assertEqual(user.email, "bla@bla.bla")
        message = self.getmessage(response)
        self.assertIn("success", message.tags)
        self.assertIn("You can now start creating your page.",
                      message.message)

    def test_register_unconfirmed_email(self):
        user = UserModel.objects.create_user(username="bla@bla.bla",
                                             email="bla@bla.bla")
        url = reverse("users:register")
        response = self.client.post(url,
                                    {'email': user.email})
        self.assertRedirects(response, reverse("users:emailsent"))
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject,
                         'Finalize your registration')

    def test_register_confirmed_email(self):
        user = UserModel.objects.create_user(username="bla@bla.bla",
                                             email="bla@bla.bla",
                                             password="testblapass")
        user.profile.email_confirmed = True
        user.profile.save()
        url = reverse("users:register")
        response = self.client.post(url,
                                    {'email': user.email})
        self.assertRedirects(response, reverse("users:emailsent"))
        self.assertEqual(len(mail.outbox), 0)

    def test_submit_invalid_email(self):
        url = reverse("users:register")
        response = self.client.post(url,
                                    {'email': ""})
        self.assertFormError(response, "form", "email",
                             "This field is required.")
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(url,
                                    {'email': "dfadöasd"})
        self.assertFormError(response, "form", "email",
                             "Enter a valid email address.")
        self.assertEqual(len(mail.outbox), 0)

    def test_set_password(self):
        user = UserModel.objects.create_user(username="bla@bla.bla",
                                             email="bla@bla.bla")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
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
                                        {'new_password1': 'ncfdjvafödia',
                                         'new_password2': 'ncfdjvafödia',
                                         'submit': ''}, follow=True)
        self.assertRedirects(postresponse, reverse('users:login'))
        user.refresh_from_db()
        user.profile.refresh_from_db()
        self.assertTrue(user.check_password("ncfdjvafödia"))
        self.assertTrue(user.profile.email_confirmed)
        message = self.getmessage(postresponse)
        self.assertEqual(message.tags, "success")
        self.assertIn("Thanks for registering.",
                      message.message)

        url = reverse("users:setpw", kwargs={"uidb64": uid,
                                             "token": token})
        response = self.client.get(url)
        self.assertFalse(response.context_data['validlink'])


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user("test@test.tt",
                                                  email="test@test.tt",
                                                  password="test")
        self.user.profile.email_confirmed = True
        self.user.profile.save()

    def test_submit_invalid_email(self):
        url = reverse("users:login")
        response = self.client.post(url,
                                    {'username': "",
                                     "password": "test"})
        self.assertFormError(response, "form", "username",
                             "This field is required.")
        response = self.client.post(url,
                                    {'username': "dfadöasd",
                                     "password": "test"})
        self.assertFormError(response, "form", "username",
                             "Enter a valid email address.")

    def test_redirect_no_pages(self):
        url = reverse("users:login")
        response = self.client.post(url,
                                    {'username': "test@test.tt",
                                     "password": "test"})
        self.assertRedirects(response, reverse("pages:createpage"))

    def test_redirect_has_pages(self):
        Page.objects.create(title="test", user=self.user)
        url = reverse("users:login")
        response = self.client.post(url,
                                    {'username': "test@test.tt",
                                     "password": "test"})
        self.assertRedirects(response, reverse("pages:pagelist"))


class PasswordChangeTestCase(MessageTestMixin, TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user("testuser",
                                                  email="test@test.tt",
                                                  password="test")

    def test_access_with_nonconfirmed_email(self):
        self.client.login(username=self.user.username, password="test")
        url = reverse("users:changepw")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("users:login") +
                             "?next=/users/changepassword/")

    def test_confirmed_email(self):
        self.user.profile.email_confirmed = True
        self.user.profile.save()
        self.client.login(username=self.user.username, password="test")
        url = reverse("users:changepw")
        response = self.client.post(url,
                                    {'old_password': 'test',
                                     'new_password1': "blablabla",
                                     'new_password2': "blablabla"},
                                    follow=True)
        self.assertRedirects(response, reverse("home:home"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("blablabla"))
        message = self.getmessage(response)
        self.assertEqual(message.tags, "success")
        self.assertIn("Your password was changed successfully.",
                      message.message)
