from django.forms import ModelForm, ChoiceField, CharField
from django.utils.translation import ugettext_lazy as _

from .models import MODULES, Page, GeneralInfoModule, FreeTextModule, \
                    FreeListModule
from .fields import ItemTextWidget, DynamicSplitArrayField


class PageCreateForm(ModelForm):
    module = ChoiceField(label=_("Choose a module to start with"),
                         choices=MODULES,
                         help_text=_("You can add more modules later"))

    class Meta:
        model = Page
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = _("Choose a title for your page")


class AddModuleForm(ModelForm):
    module = ChoiceField(label=_("Choose another module"),
                         choices=MODULES,
                         help_text=_("You can add more modules or go to "
                                     "the next step when you are finished"))

    class Meta:
        model = Page
        fields = ['title']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     raise ValidationError("You have forgotten about Fred!")
    #     return cleaned_data


class GeneralInfoModuleForm(ModelForm):
    class Meta:
        model = GeneralInfoModule
        fields = ['name', 'identity']


class FreeTextModuleForm(ModelForm):
    class Meta:
        model = FreeTextModule
        fields = ['title', 'text']


class FreeListModuleForm(ModelForm):
    items = DynamicSplitArrayField(CharField(required=False,
                                             widget=ItemTextWidget),
                                   required=False,
                                   max_size=50,
                                   remove_nulls=True,
                                   help_text=_("Click the plus-sign at the "
                                               "end of the last item to add "
                                               "more items. Empty lines will "
                                               "be ignored."))

    class Meta:
        model = FreeListModule
        fields = ['title', 'items']

    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
