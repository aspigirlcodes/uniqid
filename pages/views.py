from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import Page, GeneralInfoModule, FreeTextModule, FreeListModule,\
                    CommunicationModule, FreePictureModule, \
                    DoDontModule, MedicationModule, MedicationItem, \
                    ContactModule, SensoryModule
from .forms import PageCreateForm, GeneralInfoModuleForm, AddModuleForm,\
                   FreeTextModuleForm, FreeListModuleForm,\
                   CommunicationModuleForm, PictureFormSet, \
                   DoDontModuleForm, IntakeFormSet, SensoryModuleForm, \
                   ContactFormSet, CommunicationMethodsFormset, \
                   MedicationItemForm, ContactModuleForm, FreePictureModuleForm


class PageCreateView(CreateView):
    model = Page
    form_class = PageCreateForm
    template_name = "pages/createpage.html"

    def form_valid(self, form):
        self.object = form.save()
        url_name = "pages:create" + form.cleaned_data['module']
        url = reverse(url_name, args=[self.object.id, ])
        return HttpResponseRedirect(url)


class SelectModuleView(UpdateView):
    model = Page
    form_class = AddModuleForm
    template_name = "pages/createpage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.object.get_all_modules_sorted()
        return context

    def form_valid(self, form):
        self.object = form.save()
        if "submit_next" in self.request.POST:
            url = reverse("pages:pagepreview", args=[self.object.id, ])
        else:
            url_name = "pages:create" + form.cleaned_data['module']
            url = reverse(url_name, args=[self.object.id, ])
        return HttpResponseRedirect(url)


class ModuleCreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.page = Page.objects.get(id=self.kwargs.get('page_id'))
        context['page'] = self.page
        return context

    def form_valid(self, form):
        self.page = Page.objects.get(id=self.kwargs.get('page_id'))
        if (not form.is_empty()) or hasattr(self, "formset"):
            self.object = form.save(commit=False)
            self.object.page = self.page
            self.object.position = self.page.module_num + 1
            self.object.save()
            self.page.module_num += 1
            self.page.save()
        url = reverse("pages:addmodule", args=[self.page.id, ])
        return HttpResponseRedirect(url)


class FormsetModuleCreateView(ModuleCreateView):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, "formset_name"):
            raise NotImplementedError("'formset_name' is not defined")
        if not hasattr(self, "formset"):
            raise NotImplementedError("'formset' is not defined")
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            if self.request.FILES:
                context[self.formset_name] = self.formset(self.request.POST,
                                                          self.request.FILES)
            else:
                context[self.formset_name] = self.formset(self.request.POST)
        else:
            context[self.formset_name] = self.formset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context[self.formset_name]
        if formset.is_valid():
            # this saves the form, adds self.object, and returns redirect url
            redirect_url = super().form_valid(form)
            formset.instance = self.object
            if (not formset.save()) and form.is_empty():
                self.object.delete()
            return redirect_url
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModuleDeleteView(DeleteView):
    template_name = "pages/deletemodule.html"

    def get_success_url(self):
        page_id = self.kwargs.get('page_id')
        return reverse("pages:addmodule", args=[page_id, ])


class GeneralInfoModuleCreateView(ModuleCreateView):
    model = GeneralInfoModule
    form_class = GeneralInfoModuleForm
    template_name = "pages/creategeneralinfomodule.html"


class GeneralInfoModuleDeleteView(ModuleDeleteView):
    model = GeneralInfoModule


class CommunicationModuleCreateView(FormsetModuleCreateView):
    model = CommunicationModule
    form_class = CommunicationModuleForm
    template_name = "pages/createcommunicationmodule.html"
    formset_name = "methods_formset"
    formset = CommunicationMethodsFormset


class CommunicationModuleDeleteView(ModuleDeleteView):
    model = CommunicationModule


class DoDontModuleCreateView(ModuleCreateView):
    model = DoDontModule
    form_class = DoDontModuleForm
    template_name = "pages/createdodontmodule.html"


class DoDontModuleDeleteView(ModuleDeleteView):
    model = DoDontModule


class MedicationModuleCreateView(ModuleCreateView):
    model = MedicationItem
    form_class = MedicationItemForm
    template_name = "pages/createmedicationmodule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module_id = self.kwargs.get('module_id', None)
        if module_id:
            self.module = MedicationModule.objects.get(id=module_id)
            context['module'] = self.module
        else:
            self.module = None
        if self.request.POST:
            context['intake_formset'] = IntakeFormSet(self.request.POST)
        else:
            context['intake_formset'] = IntakeFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['intake_formset']
        if formset.is_valid():
            # create module if it doesn't exist yet
            if not self.module:
                self.module = MedicationModule.objects.create(
                    page=self.page, position=self.page.module_num + 1)
                self.page.module_num += 1
                self.page.save()
            # save MedicationItem
            self.object = form.save(commit=False)
            self.object.module = self.module
            self.object.save()
            # save intakes
            formset.instance = self.object
            if (not formset.save()) and form.is_empty():
                self.object.delete()
                if "submit_add_more" not in self.request.POST and \
                        not self.module.medicationitem_set.exists():
                    self.module.delete()
            # redirect
            if "submit_add_more" in self.request.POST:
                url = reverse("pages:updatemedicationmodule",
                              args=[self.page.id, self.module.id])
            else:
                url = reverse("pages:addmodule", args=[self.page.id, ])
            return HttpResponseRedirect(url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class MedicationModuleDeleteView(ModuleDeleteView):
    model = MedicationModule


class ContactModuleCreateView(FormsetModuleCreateView):
    model = ContactModule
    form_class = ContactModuleForm
    template_name = "pages/createcontactmodule.html"
    formset_name = "contact_formset"
    formset = ContactFormSet


class ContactModuleDeleteView(ModuleDeleteView):
    model = ContactModule


class SensoryModuleCreateView(ModuleCreateView):
    model = SensoryModule
    form_class = SensoryModuleForm
    template_name = "pages/createsensorymodule.html"


class SensoryModuleDeleteView(ModuleDeleteView):
    model = SensoryModule


class FreeTextModuleCreateView(ModuleCreateView):
    model = FreeTextModule
    form_class = FreeTextModuleForm
    template_name = "pages/createfreetextmodule.html"


class FreeTextModuleDeleteView(ModuleDeleteView):
    model = FreeTextModule


class FreeListModuleCreateView(ModuleCreateView):
    model = FreeListModule
    form_class = FreeListModuleForm
    template_name = "pages/createfreelistmodule.html"


class FreeListModuleDeleteView(ModuleDeleteView):
    model = FreeListModule


class FreePictureModuleCreateView(FormsetModuleCreateView):
    model = FreePictureModule
    template_name = "pages/createfreepicturemodule.html"
    form_class = FreePictureModuleForm
    formset_name = "picture_formset"
    formset = PictureFormSet


class FreePictureModuleDeleteView(ModuleDeleteView):
    model = FreePictureModule


class PagePreview(DetailView):
    model = Page
    template_name = "pages/page_preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.object.get_all_modules_sorted()
        return context
