from itertools import chain
from operator import attrgetter
from django.db import models
from django.utils.translation import ugettext as _

MODULES = (
    ("generalinfomodule", _("General info module")),
    ("freetextmodule", _("Free text module"))
)


class Page(models.Model):
    title = models.CharField(verbose_name=_("Page Title"), max_length=255,
                             default="", blank=True)
    module_num = models.PositiveIntegerField(default=0, blank=True)

    def get_all_modules(self):
        return {
            'generalinfomodule': self.generalinfomodule_set.all(),
            'freetextmodule': self.freetextmodule_set.all(),
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


class FreeTextModule(Module):

    template = "pages/_freetext.html"

    title = models.CharField(verbose_name=_("Title"),
                             max_length=255, default="", blank=True)
    text = models.TextField(verbose_name=_("Text"), default="", blank=True)

    def __str__(self):
        return "{page} Freetextmodule: {title}"\
            .format(page=str(self.page), title=self.title)
