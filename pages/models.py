from django.db import models
# Create your models here.

MODULES = (
    ("generalinfomodule", "General info module"),
    ("freetextmodule", "Free text module")
)


class Page(models.Model):
    title = models.CharField(max_length=255, default="", blank=True)
    module_num = models.PositiveIntegerField(default=0, blank=True)

    def get_all_modules(self):
        return {
            'generalinfomodule': self.generalinfomodule_set.all(),
            'freetextmodule': self.freetextmodule_set.all(),
        }

    def __str__(self):
        return self.title


class Module(models.Model):
    class Meta:
        abstract = True
    page = models.ForeignKey(Page)
    position = models.IntegerField()


class GeneralInfoModule(Module):
    ID_AUTISTIC = "01_autistic"
    ID_HAVE_AUT = "02_have_aut"
    ID_SPECTRUM = "03_spectrum"
    ID_ASD = "04_asd"
    ID_NEURODIV = "05_neurodiv"
    ID_ASP_SYN = "06_asp_syn"
    ID_ASPIE = "07_aspie"

    IDENTITIES = (
        (ID_AUTISTIC, "I am autistic"),
        (ID_HAVE_AUT, "I have autism"),
        (ID_SPECTRUM, "I am on the autism spectrum"),
        (ID_ASD, "I have an autism spectrum disorder"),
        (ID_NEURODIV, "I am neurodivergent"),
        (ID_ASP_SYN, "I have aspergers syndrome"),
        (ID_ASPIE, "I am an aspie"),
    )

    name = models.CharField(max_length=255, default="", blank=True)
    identity = models.CharField(max_length=32,
                                choices=IDENTITIES,
                                default="",
                                blank=True)

    def __str__(self):
        return "{page} Generalinfomodule: {name}, {id}"\
            .format(page=str(self.page), name=self.name, id=self.identity)


class FreeTextModule(Module):
    title = models.CharField(max_length=255, default="", blank=True)
    text = models.TextField(default="", blank=True)

    def __str__(self):
        return "{page} Freetextmodule: {title}"\
            .format(page=str(self.page), title=self.title)
