from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import Page, GeneralInfoModule, CommunicationModule, \
                     CommunicationMethods, MedicationItem, MedicationIntake, \
                     ModuleContact, FreeTextModule, FreeListModule, \
                     ModulePicture


class CreateGeneralinfoModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage")

    def test_create(self):
        url = reverse('pages:creategeneralinfomodule',
                      args=[str(self.page.id)])
        response = self.client.post(url,
                                    {'identity': '01_autistic',
                                     'name': 'dsfad',
                                     'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = GeneralInfoModule.objects.get(name='dsfad')
        self.assertEqual(module.page, self.page)
        self.assertEqual(module.identity, GeneralInfoModule.ID_AUTISTIC)

    def test_create_empty(self):
        url = reverse('pages:creategeneralinfomodule',
                      args=[str(self.page.id)])
        response = self.client.post(url,
                                    {'identity': '',
                                     'name': '',
                                     'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.generalinfomodule_set.count(), 0)


class CreateCommunicationModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage")

    def test_create(self):
        url = reverse('pages:createcommunicationmodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'communicationmethods_set-0-situation': 'dfad',
             'communicationmethods_set-0-me_to_you_choices': '01_spoken',
             'communicationmethods_set-0-me_to_you_free_0': '',
             'communicationmethods_set-0-you_to_me_free_0': 'dsafd',
             'communicationmethods_set-INITIAL_FORMS': '0',
             'communicationmethods_set-MAX_NUM_FORMS': '1000',
             'communicationmethods_set-MIN_NUM_FORMS': '0',
             'communicationmethods_set-TOTAL_FORMS': '1',
             'suggestions_choices': '03_pictures',
             'suggestions_free_0': '',
             'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = self.page.communicationmodule_set.first()
        self.assertEqual(module.communicationmethods_set.count(), 1)
        self.assertEqual(module.suggestions_choices,
                         [CommunicationModule.PICTURES])

    def test_create_empty_formset(self):
        url = reverse('pages:createcommunicationmodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'communicationmethods_set-0-situation': '',
             'communicationmethods_set-0-me_to_you_free_0': '',
             'communicationmethods_set-0-you_to_me_free_0': '',
             'communicationmethods_set-INITIAL_FORMS': '0',
             'communicationmethods_set-MAX_NUM_FORMS': '1000',
             'communicationmethods_set-MIN_NUM_FORMS': '0',
             'communicationmethods_set-TOTAL_FORMS': '1',
             'suggestions_choices': '03_pictures',
             'suggestions_free_0': '',
             'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = self.page.communicationmodule_set.first()
        self.assertEqual(module.communicationmethods_set.count(), 0)
        self.assertEqual(module.suggestions_choices,
                         [CommunicationModule.PICTURES])

    def test_create_empty_form(self):
        url = reverse('pages:createcommunicationmodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'communicationmethods_set-0-situation': 'dfad',
             'communicationmethods_set-0-me_to_you_choices': '01_spoken',
             'communicationmethods_set-0-me_to_you_free_0': '',
             'communicationmethods_set-0-you_to_me_free_0': 'dsafd',
             'communicationmethods_set-INITIAL_FORMS': '0',
             'communicationmethods_set-MAX_NUM_FORMS': '1000',
             'communicationmethods_set-MIN_NUM_FORMS': '0',
             'communicationmethods_set-TOTAL_FORMS': '1',
             'suggestions_free_0': '',
             'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = self.page.communicationmodule_set.first()
        self.assertEqual(module.communicationmethods_set.count(), 1)
        self.assertEqual(module.suggestions_choices, [])
        self.assertEqual(module.suggestions_free, [])

    def test_create_empty_all(self):
        url = reverse('pages:createcommunicationmodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'communicationmethods_set-0-situation': '',
             'communicationmethods_set-0-me_to_you_free_0': '',
             'communicationmethods_set-0-you_to_me_free_0': '',
             'communicationmethods_set-INITIAL_FORMS': '0',
             'communicationmethods_set-MAX_NUM_FORMS': '1000',
             'communicationmethods_set-MIN_NUM_FORMS': '0',
             'communicationmethods_set-TOTAL_FORMS': '1',
             'suggestions_free_0': '',
             'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.communicationmodule_set.count(), 0)
        self.assertEqual(CommunicationMethods.objects.count(), 0)


class CreateDoDontModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage")

    def test_create(self):
        url = reverse('pages:createdodontmodule',
                      args=[str(self.page.id)])
        response = self.client.post(url,
                                    {'ask_free_0': 'dsafdaf',
                                     'ask_free_1': 'safdasf',
                                     'do_choices': '04_do_headphones',
                                     'do_free_0': '',
                                     'dont_choices': '03_dont_questions',
                                     'dont_free_0': 'dsafvd',
                                     'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = self.page.dodontmodule_set.first()
        self.assertEqual(module.ask_free, ['dsafdaf', 'safdasf'])

    def test_create_empty(self):
        url = reverse('pages:createdodontmodule',
                      args=[str(self.page.id)])
        response = self.client.post(url,
                                    {'ask_free_0': '',
                                     'ask_free_1': '',
                                     'do_free_0': '',
                                     'dont_free_0': '',
                                     'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.dodontmodule_set.count(), 0)


class CreateMedicationModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage")

    def test_create(self):
        url = reverse('pages:createmedicationmodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'medicationintake_set-0-quantity': 'dsafd',
             'medicationintake_set-0-time': 'dsaf',
             'medicationintake_set-1-quantity': 'sew',
             'medicationintake_set-1-time': 'eds',
             'medicationintake_set-INITIAL_FORMS': '0',
             'medicationintake_set-MAX_NUM_FORMS': '1000',
             'medicationintake_set-MIN_NUM_FORMS': '0',
             'medicationintake_set-TOTAL_FORMS': '2',
             'name': 'dsafdaf',
             'remarks': 'bla',
             'submit_finish': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = self.page.medicationmodule_set.first()
        medicationitem = module.medicationitem_set.first()
        self.assertEqual(medicationitem.medicationintake_set.count(), 2)
        self.assertEqual(medicationitem.remarks, 'bla')

    def test_create_another(self):
        url = reverse('pages:createmedicationmodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'medicationintake_set-0-quantity': 'dsafd',
             'medicationintake_set-0-time': 'dsaf',
             'medicationintake_set-1-quantity': 'sew',
             'medicationintake_set-1-time': 'eds',
             'medicationintake_set-INITIAL_FORMS': '0',
             'medicationintake_set-MAX_NUM_FORMS': '1000',
             'medicationintake_set-MIN_NUM_FORMS': '0',
             'medicationintake_set-TOTAL_FORMS': '2',
             'name': 'dsafdaf',
             'remarks': 'bla',
             'submit_add_more': ''})
        module = self.page.medicationmodule_set.first()
        update_url = reverse("pages:createmoremedicationmodule",
                             args=[self.page.id, module.id])
        self.assertRedirects(response, update_url)
        self.assertEqual(module.medicationitem_set.count(), 1)
        medicationitem = module.medicationitem_set.first()
        self.assertEqual(medicationitem.medicationintake_set.count(), 2)
        self.assertEqual(medicationitem.remarks, 'bla')
        # add a second medicationitem to this
        response_2 = self.client.post(
            update_url,
            {'medicationintake_set-0-quantity': 'dsafd',
             'medicationintake_set-0-time': 'dsaf',
             'medicationintake_set-INITIAL_FORMS': '0',
             'medicationintake_set-MAX_NUM_FORMS': '1000',
             'medicationintake_set-MIN_NUM_FORMS': '0',
             'medicationintake_set-TOTAL_FORMS': '1',
             'name': 'dsafdaf',
             'remarks': 'bla2',
             'submit_finish': ''})
        self.assertRedirects(response_2,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.medicationmodule_set.count(), 1)
        module = self.page.medicationmodule_set.first()
        self.assertEqual(module.medicationitem_set.count(), 2)
        medicationitem = module.medicationitem_set.last()
        self.assertEqual(medicationitem.medicationintake_set.count(), 1)
        self.assertEqual(medicationitem.remarks, 'bla2')

    def test_create_another_empty(self):
        url = reverse('pages:createmedicationmodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'medicationintake_set-0-quantity': '',
             'medicationintake_set-0-time': '',
             'medicationintake_set-INITIAL_FORMS': '0',
             'medicationintake_set-MAX_NUM_FORMS': '1000',
             'medicationintake_set-MIN_NUM_FORMS': '0',
             'medicationintake_set-TOTAL_FORMS': '1',
             'name': '',
             'remarks': '',
             'submit_add_more': ''})
        self.assertEqual(self.page.medicationmodule_set.count(), 1)
        module = self.page.medicationmodule_set.first()
        update_url = reverse("pages:createmoremedicationmodule",
                             args=[self.page.id, module.id])
        self.assertRedirects(response, update_url)
        self.assertEqual(module.medicationitem_set.count(), 0)
        self.assertEqual(MedicationIntake.objects.count(), 0)
        # add a second empty medicationitem to this
        response_2 = self.client.post(
            update_url,
            {'medicationintake_set-0-quantity': '',
             'medicationintake_set-0-time': '',
             'medicationintake_set-INITIAL_FORMS': '0',
             'medicationintake_set-MAX_NUM_FORMS': '1000',
             'medicationintake_set-MIN_NUM_FORMS': '0',
             'medicationintake_set-TOTAL_FORMS': '1',
             'name': '',
             'remarks': '',
             'submit_finish': ''})
        self.assertRedirects(response_2,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.medicationmodule_set.count(), 0)
        self.assertEqual(MedicationItem.objects.count(), 0)
        self.assertEqual(MedicationIntake.objects.count(), 0)

    def test_create_empty_formset(self):
        url = reverse('pages:createmedicationmodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'medicationintake_set-0-quantity': '',
             'medicationintake_set-0-time': '',
             'medicationintake_set-1-quantity': '',
             'medicationintake_set-1-time': '',
             'medicationintake_set-INITIAL_FORMS': '0',
             'medicationintake_set-MAX_NUM_FORMS': '1000',
             'medicationintake_set-MIN_NUM_FORMS': '0',
             'medicationintake_set-TOTAL_FORMS': '2',
             'name': 'dsafdaf',
             'remarks': 'bla',
             'submit_finish': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = self.page.medicationmodule_set.first()
        medicationitem = module.medicationitem_set.first()
        self.assertEqual(medicationitem.medicationintake_set.count(), 0)
        self.assertEqual(medicationitem.remarks, 'bla')

    def test_create_empty_form(self):
        url = reverse('pages:createmedicationmodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'medicationintake_set-0-quantity': 'bdwe',
             'medicationintake_set-0-time': 'dasfd',
             'medicationintake_set-INITIAL_FORMS': '0',
             'medicationintake_set-MAX_NUM_FORMS': '1000',
             'medicationintake_set-MIN_NUM_FORMS': '0',
             'medicationintake_set-TOTAL_FORMS': '1',
             'name': '',
             'remarks': '',
             'submit_finish': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = self.page.medicationmodule_set.first()
        medicationitem = module.medicationitem_set.first()
        self.assertEqual(medicationitem.medicationintake_set.count(), 1)
        self.assertEqual(medicationitem.remarks, '')

    def test_create_empty_all(self):
        url = reverse('pages:createmedicationmodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'medicationintake_set-0-quantity': '',
             'medicationintake_set-0-time': '',
             'medicationintake_set-INITIAL_FORMS': '0',
             'medicationintake_set-MAX_NUM_FORMS': '1000',
             'medicationintake_set-MIN_NUM_FORMS': '0',
             'medicationintake_set-TOTAL_FORMS': '1',
             'name': '',
             'remarks': '',
             'submit_finish': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.medicationmodule_set.count(), 0)
        self.assertEqual(MedicationItem.objects.count(), 0)
        self.assertEqual(MedicationIntake.objects.count(), 0)


class CreateContactModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage")

    def test_create(self):
        url = reverse('pages:createcontactmodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'modulecontact_set-0-address': '',
             'modulecontact_set-0-email': '',
             'modulecontact_set-0-extra': '',
             'modulecontact_set-0-name': 'dsaf',
             'modulecontact_set-0-phone': '',
             'modulecontact_set-0-title': 'dsa',
             'modulecontact_set-1-address': 'safdsafdsafd\r\ndsfaddsaf',
             'modulecontact_set-1-email': '',
             'modulecontact_set-1-extra': 'dsafdsaf',
             'modulecontact_set-1-name': '',
             'modulecontact_set-1-phone': '',
             'modulecontact_set-1-title': '',
             'modulecontact_set-INITIAL_FORMS': '0',
             'modulecontact_set-MAX_NUM_FORMS': '1000',
             'modulecontact_set-MIN_NUM_FORMS': '0',
             'modulecontact_set-TOTAL_FORMS': '2',
             'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = self.page.contactmodule_set.first()
        self.assertEqual(module.modulecontact_set.count(), 2)

    def test_create_empty(self):
        url = reverse('pages:createcontactmodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'modulecontact_set-0-address': '',
             'modulecontact_set-0-email': '',
             'modulecontact_set-0-extra': '',
             'modulecontact_set-0-name': '',
             'modulecontact_set-0-phone': '',
             'modulecontact_set-0-title': '',
             'modulecontact_set-INITIAL_FORMS': '0',
             'modulecontact_set-MAX_NUM_FORMS': '1000',
             'modulecontact_set-MIN_NUM_FORMS': '0',
             'modulecontact_set-TOTAL_FORMS': '1',
             'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.contactmodule_set.count(), 0)
        self.assertEqual(ModuleContact.objects.count(), 0)


class CreateFreeTextModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage")

    def test_create(self):
        url = reverse('pages:createfreetextmodule',
                      args=[str(self.page.id)])
        response = self.client.post(url,
                                    {'title': 'bla',
                                     'text': 'dsfad',
                                     'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.freetextmodule_set.count(), 1)
        module = FreeTextModule.objects.get(text='dsfad')
        self.assertEqual(module.page, self.page)
        self.assertEqual(module.title, 'bla')

    def test_create_empty(self):
        url = reverse('pages:createfreetextmodule',
                      args=[str(self.page.id)])
        response = self.client.post(url,
                                    {'title': '',
                                     'text': '',
                                     'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.freetextmodule_set.count(), 0)


class CreateFreeListModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage")

    def test_create(self):
        url = reverse('pages:createfreelistmodule',
                      args=[str(self.page.id)])
        response = self.client.post(url,
                                    {'items_0': 'dess',
                                     'items_1': 'fde',
                                     'items_2': 'wes',
                                     'submit_add_more': '',
                                     'title': 'dfadsa'})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.freelistmodule_set.count(), 1)
        module = FreeListModule.objects.get(title='dfadsa')
        self.assertEqual(module.page, self.page)
        self.assertEqual(len(module.items), 3)

    def test_create_empty(self):
        url = reverse('pages:createfreelistmodule',
                      args=[str(self.page.id)])
        response = self.client.post(url,
                                    {'title': '',
                                     'items_0': '',
                                     'items_1': '',
                                     'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.freelistmodule_set.count(), 0)


class CreateFreePictureModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage")

    def test_create(self):
        url = reverse('pages:createfreepicturemodule',
                      args=[str(self.page.id)])
        with open('pages/tests/assets/picture.png', 'rb') as image_file:
            response = self.client.post(
                url,
                {'modulepicture_set-0-description': 'dsavfsdve',
                 'modulepicture_set-0-title': 'dasfdsa',
                 'modulepicture_set-0-picture': image_file,
                 'modulepicture_set-INITIAL_FORMS': '0',
                 'modulepicture_set-MAX_NUM_FORMS': '1000',
                 'modulepicture_set-MIN_NUM_FORMS': '0',
                 'modulepicture_set-TOTAL_FORMS': '1',
                 'submit_add_more': '',
                 'title': 'dfadf'})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = self.page.freepicturemodule_set.first()
        self.assertEqual(module.modulepicture_set.count(), 1)
        self.assertEqual(module.title, 'dfadf')

    def test_create_empty_formset(self):
        url = reverse('pages:createfreepicturemodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'modulepicture_set-0-description': '',
             'modulepicture_set-0-title': '',
             'modulepicture_set-INITIAL_FORMS': '0',
             'modulepicture_set-MAX_NUM_FORMS': '1000',
             'modulepicture_set-MIN_NUM_FORMS': '0',
             'modulepicture_set-TOTAL_FORMS': '1',
             'submit_add_more': '',
             'title': 'dfadf'})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = self.page.freepicturemodule_set.first()
        self.assertEqual(module.modulepicture_set.count(), 0)
        self.assertEqual(module.title, 'dfadf')

    def test_create_empty_form(self):
        url = reverse('pages:createfreepicturemodule',
                      args=[str(self.page.id)])
        with open('pages/tests/assets/picture.png', 'rb') as image_file:
            response = self.client.post(
                url,
                {'modulepicture_set-0-description': 'dsavfsdve',
                 'modulepicture_set-0-title': 'dasfdsa',
                 'modulepicture_set-0-picture': image_file,
                 'modulepicture_set-INITIAL_FORMS': '0',
                 'modulepicture_set-MAX_NUM_FORMS': '1000',
                 'modulepicture_set-MIN_NUM_FORMS': '0',
                 'modulepicture_set-TOTAL_FORMS': '1',
                 'submit_add_more': '',
                 'title': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = self.page.freepicturemodule_set.first()
        self.assertEqual(module.modulepicture_set.count(), 1)
        self.assertEqual(module.title, '')

    def test_create_empty_all(self):
        url = reverse('pages:createfreepicturemodule',
                      args=[str(self.page.id)])
        response = self.client.post(
            url,
            {'modulepicture_set-0-description': '',
             'modulepicture_set-0-title': '',
             'modulepicture_set-INITIAL_FORMS': '0',
             'modulepicture_set-MAX_NUM_FORMS': '1000',
             'modulepicture_set-MIN_NUM_FORMS': '0',
             'modulepicture_set-TOTAL_FORMS': '1',
             'submit_add_more': '',
             'title': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.freepicturemodule_set.count(), 0)
        self.assertEqual(ModulePicture.objects.count(), 0)
