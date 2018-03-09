# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-09 08:12
from __future__ import unicode_literals
from django.core.files import File
from django.db import migrations


def create_examples(apps, schema_editor):
    # exampleuser
    User = apps.get_model('auth', 'User')
    exampleuser = User(username="exampleuser")
    exampleuser.save()
    # example 1
    Page = apps.get_model('pages', 'Page')
    examplepage1 = Page(title="Hairdresser visit",
                        is_visible=True, is_example=True, module_num=4,
                        user=exampleuser)
    examplepage1.save()
    GeneralInfoModule = apps.get_model('pages', 'GeneralInfoModule')
    ex1_module1 = GeneralInfoModule(page=examplepage1, position=1,
                                    name="Sara",
                                    identity="01_autistic",
                                    remarks="Read on to learn more about what "
                                            "autism means to me and how you "
                                            "can help me.")
    ex1_module1.save()
    CommunicationModule = apps.get_model('pages', 'CommunicationModule')
    CommunicationMethods = apps.get_model('pages', 'CommunicationMethods')
    ex1_module2 = CommunicationModule(page=examplepage1, position=2)
    ex1_module2.save()
    meth1 = CommunicationMethods(situation="In general",
                                 you_to_me_choices=[
                                    "01_spoken",
                                    "02_written"],
                                 me_to_you_choices=[
                                    "01_spoken",
                                    "02_written"],
                                 module=ex1_module2)
    meth1.save()
    meth2 = CommunicationMethods(situation="When I am stressed",
                                 you_to_me_choices=[
                                    "01_spoken",
                                    "02_written"],
                                 me_to_you_choices=[
                                    "02_written"],
                                 module=ex1_module2)
    meth2.save()
    DoDontModule = apps.get_model('pages', 'DoDontModule')
    ex1_module3 = DoDontModule(page=examplepage1, position=3,
                               do_choices=["01_do_time",
                                           "11_do_prepare"],
                               ask_choices=["02_ask_stuff"],
                               ask_free=["Ask me before using products with a "
                                         "pronounced smell"],
                               dont_choices=["03_dont_questions",
                                             "07_dont_noises"])
    ex1_module3.save()
    FreePictureModule = apps.get_model('pages', 'FreePictureModule')
    ModulePicture = apps.get_model('pages', 'ModulePicture')
    ex1_module4 = FreePictureModule(page=examplepage1, position=4,
                                    title="This is what I wnat my hair to "
                                    "look like")
    ex1_module4.save()
    pic = ModulePicture(module=ex1_module4,
                        description="As my hair is curly it will be shorter "
                        "when dry. Please don't cut it too short as I still "
                        "want to be able to bind it together in a ponytail.")
    img_open = open("pages/static/img/shoulder-length-curly-hairstyle.jpg",
                    "rb")
    django_img = File(img_open)
    pic.picture.save("picturemodule/hair.jpg", django_img, save=True)
    # Example 2
    examplepage2 = Page(title="Doctors visit",
                        is_visible=True, is_example=True, module_num=5,
                        user=exampleuser)
    examplepage2.save()
    ex2_module1 = GeneralInfoModule(page=examplepage2, position=1,
                                    name="Sara",
                                    identity="04_asd",
                                    remarks="Read on to learn more about what "
                                            "autism means to me and how you "
                                            "can help me.")
    ex2_module1.save()
    ex2_module2 = DoDontModule(page=examplepage2, position=2,
                               do_choices=["01_do_time",
                                           "10_do_instructions",
                                           "11_do_prepare"],
                               do_free=["Write important information "
                                        "down for me."],
                               ask_choices=["02_ask_stuff",
                                            "03_ask_ready"],
                               dont_choices=["01_dont_touch",
                                             "03_dont_questions"])
    ex2_module2.save()
    SensoryModule = apps.get_model("pages", "SensoryModule")
    ex2_module3 = SensoryModule(page=examplepage2, position=3,
                                sound="05_sens_v_high", light="05_sens_v_high",
                                temperature="02_sens_low",
                                extra_choices=["01_extra_fluo",
                                               "02_extra_multi",
                                               "03_extra_pain"])
    ex2_module3.save()
    MedicationModule = apps.get_model("pages", "MedicationModule")
    MedicationItem = apps.get_model("pages", "MedicationItem")
    MedicationIntake = apps.get_model("pages", "MedicationIntake")
    ex2_module4 = MedicationModule(page=examplepage2, position=4)
    ex2_module4.save()
    item1 = MedicationItem(name="Wonder pills",
                           remarks="Take with my favorite banana yogurt",
                           module=ex2_module4, position=1)
    item1.save()
    item1intake1 = MedicationIntake(time="Breakfast", quantity="2",
                                    medication=item1, position=1)
    item1intake1.save()
    item1intake2 = MedicationIntake(time="Dinner", quantity="1",
                                    medication=item1, position=2)
    item1intake2.save()
    item2 = MedicationItem(name="Sweet sirup", module=ex2_module4, position=2)
    item2.save()
    item2intake1 = MedicationIntake(time="Before sleeping", quantity="200ml",
                                    medication=item2, position=1)
    item2intake1.save()
    ContactModule = apps.get_model("pages", "ContactModule")
    ModuleContact = apps.get_model("pages", "ModuleContact")
    ex2_module5 = ContactModule(page=examplepage2, position=5)
    ex2_module5.save()
    contact = ModuleContact(title="My GP (General Practitioner)",
                            name="Dr. Jef Arzt",
                            address="Praxisstrasse 1 \n 3000 Bern",
                            phone="031 123 45 67", module=ex2_module5)
    contact.save()
    # Example 3
    examplepage3 = Page(title="Travel",
                        is_visible=True, is_example=True, module_num=3,
                        user=exampleuser)
    examplepage3.save()
    ex3_module1 = GeneralInfoModule(page=examplepage3, position=1,
                                    name="Sara",
                                    identity="02_have_aut")
    ex3_module1.save()
    FreeListModule = apps.get_model("pages", "FreeListModule")
    ex3_module2 = FreeListModule(page=examplepage3, position=2,
                                 title="This situation "
                                 "is very stressful to me",
                                 items=["I might not be able to talk or "
                                        "answer your questions",
                                        "I might be able to write if you give "
                                        "me pen and paper or type "
                                        "on my smartphone",
                                        "Please don't touch me or try to "
                                        "comfort me by talking a lot",
                                        "Please help me get back to my hotel"])
    ex3_module2.save()
    ex3_module3 = ContactModule(page=examplepage3, position=3)
    ex3_module3.save()
    contact1 = ModuleContact(title="Hotel Imperial",
                             address="Gran Via de les Corts Catalanes, 668 \n"
                             "08010 Barcelona,\n"
                             "Spanien", phone="+34 935 10 11 30",
                             module=ex3_module3)
    contact1.save()
    contact2 = ModuleContact(title="Emergency contact", name="John Doe",
                             phone="+41 76 123 45 67", module=ex3_module3)
    contact2.save()


def delete_examples(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username="exampleuser").delete()

    Page = apps.get_model('pages', 'Page')
    Page.objects.filter(is_example=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0020_page_is_example'),
        ('auth', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_examples, delete_examples),
    ]
