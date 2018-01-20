from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import Page, GeneralInfoModule, CommunicationModule, DoDontModule


class SortModulesTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage", module_num=3)
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
