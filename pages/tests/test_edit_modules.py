from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.images import ImageFile
from ..models import Page, GeneralInfoModule, CommunicationModule, \
                     CommunicationMethods, MedicationItem, MedicationIntake, \
                     ModuleContact, FreeTextModule, FreeListModule, \
                     ModulePicture, DoDontModule, MedicationModule, \
                     ContactModule, FreePictureModule


class EditGeneralinfoModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage", module_num=1)
        self.module = GeneralInfoModule.objects.create(page=self.page,
                                                       name="sara",
                                                       position=1)

    def test_edit(self):
        url = reverse('pages:updategeneralinfomodule',
                      args=[str(self.module.id)])
        response = self.client.post(url,
                                    {'identity': '01_autistic',
                                     'name': 'dsfad',
                                     'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = GeneralInfoModule.objects.get(name='dsfad')
        self.assertEqual(module.page, self.page)
        self.assertEqual(module.identity, GeneralInfoModule.ID_AUTISTIC)

    def test_delete(self):
        url = reverse('pages:deletegeneralinfomodule',
                      args=[str(self.module.id)])
        response = self.client.post(url, {'delete': ''})
        self.page.refresh_from_db()
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.generalinfomodule_set.count(), 0)
        self.assertEqual(self.page.module_num, 0)


class EditCommunicationModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage", module_num=1)
        self.module = CommunicationModule.objects.create(
            page=self.page, suggestions_free=["help me"], position=1)

    def test_edit(self):
        url = reverse('pages:updatecommunicationmodule',
                      args=[str(self.module.id)])
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
        self.assertEqual(module.suggestions_free, [])

    def test_delete(self):
        url = reverse('pages:deletecommunicationmodule',
                      args=[str(self.module.id)])
        response = self.client.post(url, {'delete': ''})
        self.page.refresh_from_db()
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.communicationmodule_set.count(), 0)
        self.assertEqual(CommunicationMethods.objects.count(), 0)
        self.assertEqual(self.page.module_num, 0)


class EditDoDontModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage", module_num=1)
        self.module = DoDontModule.objects.create(
            page=self.page, do_choices=[DoDontModule.DO_QUIET], position=1)

    def test_edit(self):
        url = reverse('pages:updatedodontmodule',
                      args=[str(self.module.id)])
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

    def test_delete(self):
        url = reverse('pages:deletedodontmodule',
                      args=[str(self.module.id)])
        response = self.client.post(url, {'delete': ''})
        self.page.refresh_from_db()
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.dodontmodule_set.count(), 0)
        self.assertEqual(self.page.module_num, 0)


class EditMedicationModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage", module_num=1)
        self.module = MedicationModule.objects.create(page=self.page,
                                                      position=1)
        self.item = MedicationItem.objects.create(module=self.module,
                                                  name="mymed")
        self.intake1 = MedicationIntake.objects.create(medication=self.item,
                                                       quantity=5,
                                                       time="evening")

    def test_edit(self):
        url = reverse('pages:updatemedicationmodule',
                      args=[str(self.item.id)])
        response = self.client.post(
            url,
            {'medicationintake_set-0-id': str(self.intake1.id),
             'medicationintake_set-0-medication': str(self.item.id),
             'medicationintake_set-0-quantity': 'dsafd',
             'medicationintake_set-0-time': 'dsaf',
             'medicationintake_set-1-quantity': 'sew',
             'medicationintake_set-1-time': 'eds',
             'medicationintake_set-INITIAL_FORMS': '1',
             'medicationintake_set-MAX_NUM_FORMS': '1000',
             'medicationintake_set-MIN_NUM_FORMS': '0',
             'medicationintake_set-TOTAL_FORMS': '2',
             'name': 'dsafdaf',
             'remarks': 'bla',
             'submit': ''})
        self.assertRedirects(response,
                             reverse("pages:medicationmoduledetail",
                                     args=[self.module.id, ]))
        self.module.refresh_from_db()
        self.item.refresh_from_db()
        self.assertEqual(self.item.medicationintake_set.count(), 2)
        self.assertEqual(self.item.remarks, 'bla')
        self.page.refresh_from_db()
        self.assertEqual(self.page.module_num, 1)

    def test_delete_module(self):
        url = reverse('pages:deletemedicationmodule',
                      args=[str(self.module.id)])
        response = self.client.post(url, {'delete': ''})
        self.page.refresh_from_db()
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.medicationmodule_set.count(), 0)
        self.assertEqual(MedicationItem.objects.count(), 0)
        self.assertEqual(MedicationIntake.objects.count(), 0)
        self.assertEqual(self.page.module_num, 0)

    def test_delete_medicationitem(self):
        url = reverse('pages:deletemedicationitem',
                      args=[str(self.item.id)])
        response = self.client.post(url, {'delete': ''})
        self.page.refresh_from_db()
        self.assertRedirects(response,
                             reverse("pages:medicationmoduledetail",
                                     args=[self.module.id, ]))
        self.assertEqual(self.page.medicationmodule_set.count(), 1)
        self.assertEqual(MedicationItem.objects.count(), 0)
        self.assertEqual(MedicationIntake.objects.count(), 0)
        self.assertEqual(self.page.module_num, 1)


class EditContactModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage", module_num=1)
        self.module = ContactModule.objects.create(page=self.page,
                                                   position=1)
        self.contact = ModuleContact.objects.create(module=self.module,
                                                    address="bla",
                                                    title="bla")

    def test_edit(self):
        url = reverse('pages:updatecontactmodule',
                      args=[str(self.module.id)])
        response = self.client.post(
            url,
            {'modulecontact_set-0-id': str(self.contact.id),
             'modulecontact_set-0-module': str(self.module.id),
             'modulecontact_set-0-address': '',
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
             'modulecontact_set-INITIAL_FORMS': '1',
             'modulecontact_set-MAX_NUM_FORMS': '1000',
             'modulecontact_set-MIN_NUM_FORMS': '0',
             'modulecontact_set-TOTAL_FORMS': '2',
             'submit_add_more': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        module = self.page.contactmodule_set.first()
        self.assertEqual(module.modulecontact_set.count(), 2)
        self.page.refresh_from_db()
        self.contact.refresh_from_db()
        self.assertEqual(self.page.module_num, 1)
        self.assertEqual(self.contact.name, "dsaf")

    def test_delete(self):
        url = reverse('pages:deletecontactmodule',
                      args=[str(self.module.id)])
        response = self.client.post(
            url,
            {'delete': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.contactmodule_set.count(), 0)
        self.assertEqual(ModuleContact.objects.count(), 0)
        self.page.refresh_from_db()
        self.assertEqual(self.page.module_num, 0)


class EditFreeTextModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage", module_num=1)
        self.module = FreeTextModule.objects.create(page=self.page,
                                                    position=1,
                                                    title="blabla")

    def test_edit(self):
        url = reverse('pages:updatefreetextmodule',
                      args=[str(self.module.id)])
        response = self.client.post(url,
                                    {'title': 'bla',
                                     'text': 'dsfad',
                                     'submit': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.freetextmodule_set.count(), 1)
        module = FreeTextModule.objects.get(text='dsfad')
        self.assertEqual(module.page, self.page)
        self.assertEqual(module.title, 'bla')
        self.page.refresh_from_db()
        self.assertEqual(self.page.module_num, 1)

    def test_delete(self):
        url = reverse('pages:deletefreetextmodule',
                      args=[str(self.module.id)])
        response = self.client.post(url, {'delete': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.freetextmodule_set.count(), 0)
        self.page.refresh_from_db()
        self.assertEqual(self.page.module_num, 0)


class EditFreeListModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage", module_num=1)
        self.module = FreeListModule.objects.create(page=self.page,
                                                    position=1,
                                                    title="bla")

    def test_edit(self):
        url = reverse('pages:updatefreelistmodule',
                      args=[str(self.module.id)])
        response = self.client.post(url,
                                    {'items_0': 'dess',
                                     'items_1': 'fde',
                                     'items_2': 'wes',
                                     'submit': '',
                                     'title': 'dfadsa'})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.freelistmodule_set.count(), 1)
        module = FreeListModule.objects.get(title='dfadsa')
        self.assertEqual(module.page, self.page)
        self.assertEqual(len(module.items), 3)
        self.page.refresh_from_db()
        self.assertEqual(self.page.module_num, 1)

    def test_delete(self):
        url = reverse('pages:deletefreelistmodule',
                      args=[str(self.module.id)])
        response = self.client.post(url, {'delete': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.freelistmodule_set.count(), 0)
        self.page.refresh_from_db()
        self.assertEqual(self.page.module_num, 0)


class CreateFreePictureModuleTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="testpage", module_num=1)
        self.module = FreePictureModule.objects.create(page=self.page,
                                                       position=1,
                                                       title="bla")
        with open('pages/tests/assets/picture.png', 'rb') as image_file:
            self.image = ModulePicture.objects.create(
                module=self.module, picture=ImageFile(image_file))

    def test_edit(self):
        url = reverse('pages:updatefreepicturemodule',
                      args=[str(self.module.id)])
        with open('pages/tests/assets/picture.png', 'rb') as image_file:
            response = self.client.post(
                url,
                {'modulepicture_set-0-id': str(self.image.id),
                 'modulepicture_set-0-module': str(self.module.id),
                 'modulepicture_set-0-description': 'dsavfsdve',
                 'modulepicture_set-0-title': 'dasfdsa',
                 'modulepicture_set-0-picture': image_file,
                 'modulepicture_set-INITIAL_FORMS': '1',
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
        self.page.refresh_from_db()
        self.assertEqual(self.page.module_num, 1)

    def test_delete(self):
        url = reverse('pages:deletefreepicturemodule',
                      args=[str(self.module.id)])
        response = self.client.post(url, {'delete': ''})
        self.assertRedirects(response,
                             reverse("pages:addmodule", args=[self.page.id, ]))
        self.assertEqual(self.page.freepicturemodule_set.count(), 0)
        self.assertEqual(ModulePicture.objects.count(), 0)
        self.page.refresh_from_db()
        self.assertEqual(self.page.module_num, 0)
