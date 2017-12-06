from django.forms import ModelForm, ChoiceField, CharField
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from .models import MODULES, Page, GeneralInfoModule, FreeTextModule, \
                    FreeListModule, CommunicationMethodsModule, \
                    FreePictureModule, ModulePicture
from .fields import ItemTextWidget, DynamicSplitArrayField


PictureFormSet = inlineformset_factory(FreePictureModule, ModulePicture,
                                       fields=['title', 'picture',
                                               'description'],
                                       extra=1)


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


class CommunicationMethodsModuleForm(ModelForm):
    me_to_you_free = DynamicSplitArrayField(
        CharField(required=False, widget=ItemTextWidget),
        label=_("Other communication methods I might use"),
        required=False,
        max_size=50,
        remove_nulls=True,
        help_text=_("Click the plus-sign at the end of the last item to add "
                    "more items. Empty lines will be ignored."))
    you_to_me_free = DynamicSplitArrayField(
        CharField(required=False, widget=ItemTextWidget),
        label=_("Other communication methods you can use"),
        required=False,
        max_size=50,
        remove_nulls=True,
        help_text=_("Click the plus-sign at the end of the last item to add "
                    "more items. Empty lines will be ignored."))

    class Meta:
        model = CommunicationMethodsModule
        fields = ['situation', 'me_to_you_choices', 'me_to_you_free',
                  'you_to_me_choices', 'you_to_me_free']


class FreeTextModuleForm(ModelForm):
    class Meta:
        model = FreeTextModule
        fields = ['title', 'text']


class FreeListModuleForm(ModelForm):
    items = DynamicSplitArrayField(CharField(required=False,
                                             widget=ItemTextWidget),
                                   label=_("Items"),
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
