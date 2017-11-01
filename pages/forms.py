from django import forms
from .models import MODULES, Page, GeneralInfoModule


class PageCreateForm(forms.ModelForm):
    module = forms.ChoiceField(label="Choose a module to start with",
                               choices=MODULES,
                               help_text="You can add more modules later")

    class Meta:
        model = Page
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Choose a title for your page"


class AddModuleForm(forms.ModelForm):
    module = forms.ChoiceField(label="Choose another module",
                               choices=MODULES,
                               help_text="You can add more modules or go to "
                               "the next step when you are finished")

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
