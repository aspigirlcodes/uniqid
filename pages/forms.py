from django import forms
from django.utils.translation import ugettext as _

from .models import MODULES, Page, GeneralInfoModule, FreeTextModule


class PageCreateForm(forms.ModelForm):
    module = forms.ChoiceField(label=_("Choose a module to start with"),
                               choices=MODULES,
                               help_text=_("You can add more modules later"))

    class Meta:
        model = Page
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = _("Choose a title for your page")


class AddModuleForm(forms.ModelForm):
    module = forms.ChoiceField(label=_("Choose another module"),
                               choices=MODULES,
                               help_text=_("You can add more modules or go to "
                               "the next step when you are finished"))

    class Meta:
        model = Page
        fields = ['title']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     raise forms.ValidationError("You have forgotten about Fred!")
    #     return cleaned_data


class GeneralInfoModuleForm(forms.ModelForm):
    class Meta:
        model = GeneralInfoModule
        fields = ['name', 'identity']


class FreeTextModuleForm(forms.ModelForm):
    class Meta:
        model = FreeTextModule
        fields = ['title', 'text']
