from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from ..models import Page, GeneralInfoModule, CommunicationModule, DoDontModule

UserModel = get_user_model()


class CreatePageTestCase(TestCase):

    def test_create_with_user(self):
        user = UserModel.objects.create_user("testuser",
                                             password="test")
        self.client.login(username="testuser", password="test")
        url = reverse('pages:createpage')
        response = self.client.post(url,
                                    {'title': 'testpage',
                                     'module': 'generalinfomodule',
                                     'submit': ''})
        self.assertEqual(Page.objects.all().count(), 1)
        page = Page.objects.first()
        self.assertRedirects(response, reverse("pages:creategeneralinfomodule",
                                               args=[page.id, ]))
        self.assertEqual(page.user, user)


class SortModulesTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user("testuser",
                                                  email="test@test.tt",
                                                  password="test")
        self.client.login(username=self.user.username, password="test")
        self.page = Page.objects.create(title="testpage",
                                        user=self.user,
                                        module_num=3)
        self.module1 = GeneralInfoModule.objects.create(page=self.page,
                                                        name="sara",
                                                        position=1)
        self.module2 = CommunicationModule.objects.create(
            page=self.page, suggestions_free=["help me"], position=2)
        self.module3 = DoDontModule.objects.create(
            page=self.page, do_choices=[DoDontModule.DO_QUIET], position=3)

    def test_sort_valid(self):
        url = reverse('pages:sortmodules', args=[str(self.page.id)])
        response = self.client.post(url,
                                    {'position_1': '2',
                                     'position_2': '3',
                                     'position_3': '1',
                                     'submit': ''})
        self.assertRedirects(response, reverse("pages:pagepreview",
                                               args=[self.page.id, ]))
        self.module1.refresh_from_db()
        self.module2.refresh_from_db()
        self.module3.refresh_from_db()
        self.assertEqual(self.module1.position, 2)
        self.assertEqual(self.module2.position, 3)
        self.assertEqual(self.module3.position, 1)

    def test_sort_invalid(self):
        url = reverse('pages:sortmodules', args=[str(self.page.id)])
        response = self.client.post(url,
                                    {'position_1': '2',
                                     'position_2': '3',
                                     'position_3': '2',
                                     'submit': ''})
        # import ipdb; ipdb.set_trace()
        self.assertFormError(response, "form", None,
                             "You can use each position only once.")
        self.module1.refresh_from_db()
        self.module2.refresh_from_db()
        self.module3.refresh_from_db()
        self.assertEqual(self.module1.position, 1)
        self.assertEqual(self.module2.position, 2)
        self.assertEqual(self.module3.position, 3)

    def test_sort_empty_value(self):
        url = reverse('pages:sortmodules', args=[str(self.page.id)])
        response = self.client.post(url,
                                    {'position_1': '2',
                                     'position_2': '3',
                                     'submit': ''})
        # import ipdb; ipdb.set_trace()
        self.assertFormError(response, "form", "position_3",
                             "This field is required.")
        self.module1.refresh_from_db()
        self.module2.refresh_from_db()
        self.module3.refresh_from_db()
        self.assertEqual(self.module1.position, 1)
        self.assertEqual(self.module2.position, 2)
        self.assertEqual(self.module3.position, 3)


class PageListViewTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user("test@test.tt",
                                                  email="test@test.tt",
                                                  password="test")
        otheruser = UserModel.objects.create_user("otheruser@test.tt",
                                                  email="otheruser@test.tt",
                                                  password="test")
        self.client.login(username=self.user.username, password="test")
        self.page1 = Page.objects.create(title="testpage",
                                         user=self.user)
        self.page2 = Page.objects.create(title="testpage2",
                                         user=self.user, is_active=False)
        self.page3 = Page.objects.create(title="testpage3",
                                         user=otheruser)

    def test_get_queryset(self):
        url = reverse("pages:pagelist")
        response = self.client.get(url)
        self.assertContains(response, self.page1)
        self.assertNotContains(response, self.page2)
        self.assertNotContains(response, self.page3)
