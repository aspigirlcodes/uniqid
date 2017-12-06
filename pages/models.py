from itertools import chain
from operator import attrgetter
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from .fields import ChoiceArrayField

MODULES = (
    ("generalinfomodule", _("General info module")),
    ("communicationmethodsmodule", _("Communication methods module")),
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
