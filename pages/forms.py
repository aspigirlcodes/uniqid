import logging
from django.forms import ModelForm, ChoiceField, CharField, ValidationError, \
                         IntegerField
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from .models import MODULES, MODULE_HELP, Page, GeneralInfoModule, \
                    FreeTextModule, ModuleContact, ContactModule, \
                    FreeListModule, CommunicationMethods, CommunicationModule,\
                    FreePictureModule, ModulePicture, DoDontModule, \
                    MedicationItem, MedicationIntake, SensoryModule
from .fields import ItemTextWidget, DynamicSplitArrayField, RadioWithHelpSelect


logger = logging.getLogger('pages')


PictureFormSet = inlineformset_factory(FreePictureModule, ModulePicture,
                                       fields=['title', 'picture',
                                               'description'],
                                       extra=1)

IntakeFormSet = inlineformset_factory(MedicationItem, MedicationIntake,
                                      fields=['time', 'quantity'],
                                      extra=1)

ContactFormSet = inlineformset_factory(ContactModule, ModuleContact,
                                       fields=['title', 'name', 'address',
                                               'phone', 'email', 'extra'],
                                       extra=1)


class PageCreateForm(ModelForm):
    module = ChoiceField(label=_("Choose a module to start with"),
                         choices=MODULES,
                         widget=RadioWithHelpSelect(help_texts=MODULE_HELP),
                         help_text=_("You can add more modules later"))

    class Meta:
        model = Page
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = _("Choose a title for your page")


class AddModuleForm(ModelForm):
    module = ChoiceField(label=_("Or choose another module"),
                         choices=MODULES,
                         required=False,
                         widget=RadioWithHelpSelect(help_texts=MODULE_HELP))

    class Meta:
        model = Page
        fields = ['title']

    def clean_module(self):
        module = self.cleaned_data['module']
        if 'submit_module' in self.data.keys() and not module:
            raise ValidationError(_("You have to choose a module."),
                                  code="required")
        return module


class ModuleMixin(object):
    def is_empty(self):
        return not any(self.cleaned_data.values())


class GeneralInfoModuleForm(ModuleMixin, ModelForm):
    class Meta:
        model = GeneralInfoModule
        fields = ['name', 'identity']


class CommunicationModuleForm(ModuleMixin, ModelForm):
    suggestions_free = DynamicSplitArrayField(
        CharField(required=False, widget=ItemTextWidget),
        label=_("Other communication suggestions"),
        required=False,
        max_size=50,
        remove_nulls=True,
        help_text=_("Click the plus-sign at the end of the last item to add "
                    "more items. Empty lines will be ignored."))

    class Meta:
        model = CommunicationModule
        fields = ['suggestions_choices', 'suggestions_free']


class CommunicationMethodsForm(ModuleMixin, ModelForm):
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
        model = CommunicationMethods
        fields = ['situation', 'me_to_you_choices', 'me_to_you_free',
                  'you_to_me_choices', 'you_to_me_free']


CommunicationMethodsFormset = inlineformset_factory(
    CommunicationModule, CommunicationMethods, form=CommunicationMethodsForm,
    extra=1)


class DoDontModuleForm(ModuleMixin, ModelForm):
    do_free = DynamicSplitArrayField(
        CharField(required=False, widget=ItemTextWidget),
        label=_("More things others can do"),
        required=False,
        max_size=50,
        remove_nulls=True,
        help_text=_("Click the plus-sign at the end of the last item to add "
                    "more items. Empty lines will be ignored."))
    ask_free = DynamicSplitArrayField(
        CharField(required=False, widget=ItemTextWidget),
        label=_("More things others should ask"),
        required=False,
        max_size=50,
        remove_nulls=True,
        help_text=_("Click the plus-sign at the end of the last item to add "
                    "more items. Empty lines will be ignored."))
    dont_free = DynamicSplitArrayField(
        CharField(required=False, widget=ItemTextWidget),
        label=_("More things others shouldn't do"),
        required=False,
        max_size=50,
        remove_nulls=True,
        help_text=_("Click the plus-sign at the end of the last item to add "
                    "more items. Empty lines will be ignored."))

    class Meta:
        model = DoDontModule
        fields = ['do_choices', 'do_free', 'ask_choices',
                  'ask_free', 'dont_choices', 'dont_free']


class MedicationItemForm(ModuleMixin, ModelForm):
    class Meta:
        model = MedicationItem
        fields = ['name', 'remarks']


class ContactModuleForm(ModuleMixin, ModelForm):
    class Meta:
        model = ContactModule
        fields = []


class SensoryModuleForm(ModuleMixin, ModelForm):
    extra_free = DynamicSplitArrayField(
        CharField(required=False, widget=ItemTextWidget),
        label=_("More additional sensory info"),
        required=False,
        max_size=50,
        remove_nulls=True,
        help_text=_("Click the plus-sign at the end of the last item to add "
                    "more items. Empty lines will be ignored."))

    class Meta:
        model = SensoryModule
        fields = ['sound', 'light', 'smell',
                  'temperature', 'extra_choices', 'extra_free']


class FreeTextModuleForm(ModuleMixin, ModelForm):
    class Meta:
        model = FreeTextModule
        fields = ['title', 'text']


class FreeListModuleForm(ModuleMixin, ModelForm):
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


class FreePictureModuleForm(ModuleMixin, ModelForm):
    class Meta:
        model = FreePictureModule
        fields = ['title']


class ModuleSortForm(ModelForm):
    class Meta:
        model = Page
        fields = []

    def __init__(self, *args, **kwargs):
        self.page = kwargs['instance']
        super().__init__(*args, **kwargs)
        for index in range(1, self.page.module_num+1):
            field_name = "position_{}".format(index)
            self.fields[field_name] = IntegerField(
                label=_("position"), min_value=1,
                max_value=self.page.module_num,
                initial=index)

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        if len(cleaned_data) == self.page.module_num and \
                not set(cleaned_data.values()) == \
                set(range(1, self.page.module_num + 1)):
            logger.info("sort page %s submitted with wrong positions:%s",
                        self.page.id, cleaned_data.values().join(", "))
            raise(ValidationError(_("You can use each position only once."),
                                  code="double_value"))
        return cleaned_data
