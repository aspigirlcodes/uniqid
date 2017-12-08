from itertools import chain
from operator import attrgetter
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from .fields import ChoiceArrayField

MODULES = (
    ("generalinfomodule", _("General info module")),
    ("communicationmethodsmodule", _("Communication methods module")),
    ("dodontmodule", _("Do's and Don'ts module")),
    ("medicationmodule", _("Medication module")),
    ("sensorymodule", _("Sensory module")),
    ("contactmodule", _("Contact module")),
    ("freetextmodule", _("Free text module")),
    ("freelistmodule", _("Free list module")),
    ("freepicturemodule", _("Free picture module"))
)


class Page(models.Model):
    title = models.CharField(verbose_name=_("Page Title"), max_length=255,
                             default="", blank=True)
    module_num = models.PositiveIntegerField(default=0, blank=True)

    def get_all_modules(self):
        return {
            'generalinfomodule': self.generalinfomodule_set.all(),
            'communicationmethodsmodule':
                self.communicationmethodsmodule_set.all(),
            'dodontmodule': self.dodontmodule_set.all(),
            'medicationmodule': self.medicationmodule_set.all(),
            'sensorymodule': self.sensorymodule_set.all(),
            'contactmodule': self.contactmodule_set.all(),
            'freetextmodule': self.freetextmodule_set.all(),
            'freelistmodule': self.freelistmodule_set.all(),
            'freepicturemodule': self.freepicturemodule_set.all(),
        }

    def get_all_modules_sorted(self):
        module_dict = self.get_all_modules()
        return sorted(
            chain(*module_dict.values()),
            key=attrgetter('position'))

    def __str__(self):
        return self.title


class Module(models.Model):
    class Meta:
        abstract = True

    page = models.ForeignKey(Page, verbose_name=_("Page"))
    position = models.IntegerField(verbose_name=_("Position"))

    @property
    def type(self):
        return self.__class__.__name__


class GeneralInfoModule(Module):
    ID_AUTISTIC = "01_autistic"
    ID_HAVE_AUT = "02_have_aut"
    ID_SPECTRUM = "03_spectrum"
    ID_ASD = "04_asd"
    ID_NEURODIV = "05_neurodiv"
    ID_ASP_SYN = "06_asp_syn"
    ID_ASPIE = "07_aspie"

    IDENTITIES = (
        (ID_AUTISTIC, _("I am autistic")),
        (ID_HAVE_AUT, _("I have autism")),
        (ID_SPECTRUM, _("I am on the autism spectrum")),
        (ID_ASD, _("I have an autism spectrum disorder")),
        (ID_NEURODIV, _("I am neurodivergent")),
        (ID_ASP_SYN, _("I have aspergers syndrome")),
        (ID_ASPIE, _("I am an aspie")),
    )

    template = "pages/_generalinfo.html"

    name = models.CharField(verbose_name=_("Name"), max_length=255, default="",
                            blank=True)
    identity = models.CharField(verbose_name=_("Identity"),
                                max_length=32,
                                choices=IDENTITIES,
                                default="",
                                blank=True)

    def __str__(self):
        return "{page} Generalinfomodule: {name}, {id}"\
            .format(page=str(self.page), name=self.name, id=self.identity)


class CommunicationMethodsModule(Module):

    template = "pages/_communicationmethods.html"

    SPOKEN = "01_spoken"
    WRITTEN = "02_written"
    TEXT_AAC = "03_text_aac"
    PIC_AAC = "04_pic_aac"
    OFF_SIGN = "05_off_sign"
    OTHER_SIGN = "06_other_sign"

    METHODS = (
        (SPOKEN, _("Spoken language")),
        (WRITTEN, _("Written language")),
        (TEXT_AAC, _("Text based alternative to speech")),
        (PIC_AAC, _("Picture based alternative to speech")),
        (OFF_SIGN, _("Official signlanguage")),
        (OTHER_SIGN, _("Other signs, gestures or behaviours"))
    )

    situation = models.CharField(verbose_name=_("Situation"),
                                 max_length=255, default="", blank=True)
    you_to_me_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=METHODS),
        verbose_name=_("You can use"), blank=True)
    you_to_me_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("Other communication methods you can use"),
        blank=True)
    me_to_you_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=METHODS),
        verbose_name=_("I will use"), blank=True)
    me_to_you_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("Other communication methods I might use"),
        blank=True)


class DoDontModule(Module):
    template = "pages/_dodont.html"

    DO_TIME = "01_do_time"
    DO_LIGHT = "02_do_light"
    DO_QUIET = "03_do_quiet"
    DO_HEADPHONES = "04_do_headphones"
    DO_EAR_PROTECT = "05_do_ear_protect"
    DO_FIDGET = "06_do_fidget"
    DO_CALM = "07_do_calm"
    DO_CHANGES = "08_do_changes"
    DO_NOISES = "09_do_noises"
    DO_INSTRUCTIONS = "10_do_instructions"
    DO_PREPARE = "11_do_prepare"

    ASK_TOUCH = "01_ask_touch"
    ASK_STUFF = "02_ask_stuff"
    ASK_READY = "03_ask_ready"
    ASK_COMMUNICATE = "04_ask_communicate"
    ASK_TALK = "05_ask_talk"

    DONT_TOUCH = "01_dont_touch"
    DONT_EYE = "02_dont_eye"
    DONT_QUESTIONS = "03_dont_questions"
    DONT_CLOSE = "04_dont_close"
    DONT_CHITCHAT = "05_chitchat"
    DONT_TALK = "06_dont_talk"
    DONT_NOISES = "07_dont_noises"

    DOS = (
        (DO_TIME, _("Leave me enough time to answer your questions "
                    "or to make decisions")),
        (DO_LIGHT, _("Use natural light and turn off fluorescent lights "
                     "if possible")),
        (DO_QUIET, _("Try to find a quiet room or space for me")),
        (DO_HEADPHONES, _("Let me use my headphones "
                          "to listen to my favorite music")),
        (DO_EAR_PROTECT, _("Let me use my ear protection "
                           "to block out noises")),
        (DO_FIDGET, _("Let me fidget, move around, flap my arms or "
                      "make other sounds or motions")),
        (DO_CALM, _("Talk to me with a calm voice")),
        (DO_CHANGES, _("Tel me about changes in plans as soon as possible")),
        (DO_NOISES, _("Turn of the TV, radio or other things "
                      "that make noise")),
        (DO_INSTRUCTIONS, _("Give me clear instructions "
                            "if I have to do something")),
        (DO_PREPARE, _("Tell me what is going to happen beforehand"))
    )

    ASKS = (
        (ASK_TOUCH, _("Ask before you touch me")),
        (ASK_STUFF, _("Ask befor touching my stuff")),
        (ASK_READY, _("Ask me if I am ready to go (and where we go to) "
                      "befor you take me to a new place")),
        (ASK_COMMUNICATE, _("Ask me about what method of communication "
                            "I want to use")),
        (ASK_TALK, _("Ask me if I want to talk or socialize "
                     "before introducing me to new people"))
    )

    DONTS = (
        (DONT_TOUCH, _("Don't touch me without permission")),
        (DONT_EYE, _("Don't force me to make eye contact")),
        (DONT_QUESTIONS, _("Don't ask me to many questions")),
        (DONT_CLOSE, _("Do not sit or stand close to me "
                       "unless it is necessary")),
        (DONT_CHITCHAT, _("Avoid chitchat")),
        (DONT_TALK, _("Don't talk a lot to try to calm me, "
                      "as this has the contrary effect")),
        (DONT_NOISES, _("Don't make unexpected hard noises "
                        "such as slamming a door")),
    )

    do_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=DOS),
        verbose_name=_("Things others can do to help you"), blank=True)
    do_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("More things others can do"),
        blank=True)
    ask_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=ASKS),
        verbose_name=_("Things people should ask you about"), blank=True)
    ask_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("More things others should ask"),
        blank=True)
    dont_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=DONTS),
        verbose_name=_("Things others should not do"), blank=True)
    dont_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("More things others shouldn't do"),
        blank=True)


class MedicationModule(Module):
    template = "pages/_medication.html"


class MedicationItem(models.Model):
    name = models.CharField(verbose_name=_("Medication name"),
                            max_length=255, default="", blank=True)
    remarks = models.TextField(verbose_name=_("Remarks"), default="",
                               blank=True)
    module = models.ForeignKey(MedicationModule, verbose_name=_("module"))


class MedicationIntake(models.Model):
    time = models.CharField(verbose_name=_("Intake time"),
                            max_length=255, default="", blank=True)
    quantity = models.CharField(verbose_name=_("Intake quantity"),
                                max_length=255, default="", blank=True)
    medication = models.ForeignKey(MedicationItem,
                                   verbose_name=_("medication"))


class SensoryModule(Module):
    template = "pages/_sensory.html"

    SENS_NONE = "00_sens_none"
    SENS_V_LOW = "01_sens_v_low"
    SENS_LOW = "02_sens_low"
    SENS_MED = "03_sens_med"
    SENS_HIGH = "04_sens_high"
    SENS_V_HIGH = "05_sens_v_high"

    RANGE = (
        (SENS_NONE, _("Do not include")),
        (SENS_V_LOW, _("Very low")),
        (SENS_LOW, _("Lower than average")),
        (SENS_MED, _("Average")),
        (SENS_HIGH, _("Higher than average")),
        (SENS_V_HIGH, _("Very high"))
    )

    EXTRA_FLUO = "01_extra_fluo"
    EXTRA_MULTI = "02_extra_multi"
    EXTRA_PAIN = "03_extra_pain"

    EXTRAS = (
        (EXTRA_FLUO, _("I can't cope with fluorescent lighting")),
        (EXTRA_MULTI, _("I have trouble processing more than on sense at a "
                        "time, for example hearing you while looking at "
                        "something")),
        (EXTRA_PAIN, _("I have difficulties recognizing and or reporting pain "
                       "or other symptoms"))
    )

    sound = models.CharField(verbose_name=_("Sensitivity to sound"),
                             max_length=32,
                             choices=RANGE,
                             default=SENS_NONE)
    light = models.CharField(verbose_name=_("Sensitivity to light"),
                             max_length=32,
                             choices=RANGE,
                             default=SENS_NONE)
    smell = models.CharField(verbose_name=_("Sensitivity to smells"),
                             max_length=32,
                             choices=RANGE,
                             default=SENS_NONE)
    temperature = models.CharField(
        verbose_name=_("Sensitivity to temperature"),
        max_length=32,
        choices=RANGE,
        default=SENS_NONE)
    extra_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=EXTRAS),
        verbose_name=_("Additional sensory info"), blank=True)
    extra_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("More additional sensory info"),
        blank=True)

    @property
    def has_sensory_profile(self):
        return self.sound != self.SENS_NONE \
                or self.light != self.SENS_NONE \
                or self.smell != self.SENS_NONE \
                or self.temperature != self.SENS_NONE


class ContactModule(Module):
    template = "pages/_contact.html"

    title = models.CharField(verbose_name=_("Contact title"),
                             max_length=255, default="", blank=True,
                             help_text=_("Choose a descriptive title for the "
                                         "contact. A good title may include "
                                         "the role of this contact, "
                                         "or the situation in which they "
                                         "can be contacted."))
    name = models.CharField(verbose_name=_("Name"),
                            max_length=255, default="", blank=True)
    address = models.TextField(verbose_name=_("Address"), default="",
                               blank=True)
    phone = models.CharField(verbose_name=_("Phone number"),
                             max_length=255, default="", blank=True)
    email = models.EmailField(verbose_name=_("Email address"), default="",
                              blank=True)
    extra = models.TextField(verbose_name=_("Extra comment"), default="",
                             blank=True)


class FreeTextModule(Module):

    template = "pages/_freetext.html"

    title = models.CharField(verbose_name=_("Title"),
                             max_length=255, default="", blank=True)
    text = models.TextField(verbose_name=_("Text"), default="", blank=True)

    def __str__(self):
        return "{page} Freetextmodule: {title}"\
            .format(page=str(self.page), title=self.title)


class FreeListModule(Module):

    template = "pages/_freelist.html"

    title = models.CharField(verbose_name=_("Title"),
                             max_length=255, default="", blank=True)
    items = ArrayField(models.CharField(max_length=255),
                       verbose_name=_("Items"), blank=True)

    def __str__(self):
        return "{page} Freelistmodule: {title}"\
            .format(page=str(self.page), title=self.title)


class FreePictureModule(Module):

    template = "pages/_freepicture.html"

    title = models.CharField(verbose_name=_("Title"),
                             max_length=255, default="", blank=True)

    def __str__(self):
        return "{page} Freelistmodule: {title}"\
            .format(page=str(self.page), title=self.title)


class ModulePicture(models.Model):
    module = models.ForeignKey(FreePictureModule, verbose_name=_("module"))
    picture = models.ImageField(verbose_name=_("Image"), blank=True,
                                null=True)
    description = models.TextField(verbose_name=_("Image description"),
                                   null=True, blank=True)
    title = models.CharField(verbose_name=_("Image title"),
                             max_length=255, default="", blank=True)
