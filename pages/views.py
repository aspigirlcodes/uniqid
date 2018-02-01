import logging
from django.views.generic import CreateView, DetailView, UpdateView, \
                                 DeleteView, ListView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin, \
                                       LoginRequiredMixin
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from .models import Page, GeneralInfoModule, FreeTextModule, FreeListModule,\
                    CommunicationModule, FreePictureModule, \
                    DoDontModule, MedicationModule, MedicationItem, \
                    ContactModule, SensoryModule
from .forms import PageCreateForm, GeneralInfoModuleForm, AddModuleForm,\
                   FreeTextModuleForm, FreeListModuleForm,\
                   CommunicationModuleForm, PictureFormSet, \
                   DoDontModuleForm, IntakeFormSet, SensoryModuleForm, \
                   ContactFormSet, CommunicationMethodsFormset, \
                   MedicationItemForm, ContactModuleForm, \
                   FreePictureModuleForm, ModuleSortForm


logger = logging.getLogger('pages')


class PageCreateAccessMixin(LoginRequiredMixin):
    """
    LoginRequired, but instead of redirecting to login, redirect to register.
    """
    def handle_no_permission(self):
        return HttpResponseRedirect(reverse("users:register"))


class PageCreateView(PageCreateAccessMixin, CreateView):
    """
    Allow a user to create a page and add a first module.
    """
    model = Page
    form_class = PageCreateForm
    template_name = "pages/createpage.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        logger.info("user %s created a page", self.request.user.username)
        url_name = "pages:create" + form.cleaned_data['module']
        url = reverse(url_name, args=[self.object.id, ])
        return HttpResponseRedirect(url)


class SelectModuleView(UserPassesTestMixin, UpdateView):
    """
    Update page and add new modules.
    """
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
            logger.info("redirecting user %s to sort %s modules of page %s",
                        self.request.user.username,
                        self.object.module_num, self.object.id)
            url = reverse("pages:sortmodules", args=[self.object.id, ])
        else:
            logger.info("redirecting user %s to add another module to page %s",
                        self.request.user.username, self.object.id)
            url_name = "pages:create" + form.cleaned_data['module']
            url = reverse(url_name, args=[self.object.id, ])
        return HttpResponseRedirect(url)

    def test_func(self):
        return self.request.user == self.get_object().user


class ModuleCreateView(UserPassesTestMixin, CreateView):
    """
    Baseview for creating a module.
    Can be subclassed by most modulecreateviews.
    """
    def get_context_data(self, **kwargs):
        """
        Add the page to the context explicitly.
        Add form_context: create to the context so that we can use
        one template but still differentiate between create and update cases.
        """
        context = super().get_context_data(**kwargs)
        self.page = Page.objects.get(id=self.kwargs.get('page_id'))
        context['page'] = self.page
        context['form_context'] = "create"
        return context

    def form_valid(self, form):
        """
        Set the page foreignkey of the newly created model.
        Update the number of modules in the page.
        Give the module the next available position.
        Make sure to not create a module if the form was left empty.
        """
        self.page = Page.objects.get(id=self.kwargs.get('page_id'))
        if (not form.is_empty()) or hasattr(self, "formset"):
            self.object = form.save(commit=False)
            self.object.page = self.page
            self.object.position = self.page.module_num + 1
            self.object.save()
            self.page.module_num += 1
            self.page.save()
            logger.info("user %s created %s module for page %s",
                        self.request.user.username,
                        self.object.type, self.object.page.id)
        else:
            logger.info("empty %s module for page %s by user %s not added",
                        self.object.type, self.object.page.id,
                        self.request.user.username,)
        url = reverse("pages:addmodule", args=[self.page.id, ])
        return HttpResponseRedirect(url)

    def test_func(self):
        """
        Access test: Only the owner of the page can create modules for it.
        """
        page = Page.objects.get(id=self.kwargs.get('page_id'))
        return self.request.user == page.user


class FormsetModuleCreateView(ModuleCreateView):
    """
    Baseview for creating a module
    using a formset for a Foreignkey linked model.
    Can be subclassed by modulecreateviews needing to use a formset.
    """

    def __init__(self, *args, **kwargs):
        """
        Views need to set two attributes:
        formset_name
            which is what the form will be called in the
            template context.
        formset
            Formset to be used.
        """
        if not hasattr(self, "formset_name"):
            raise NotImplementedError("'formset_name' is not defined")
        if not hasattr(self, "formset"):
            raise NotImplementedError("'formset' is not defined")
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        adds the formset to the context.
        """
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
        """
        takes care of saving the formset.
        """
        context = self.get_context_data()
        formset = context[self.formset_name]
        if formset.is_valid():
            # this saves the form, adds self.object, and returns redirect url
            redirect_url = super().form_valid(form)
            formset.instance = self.object
            if (not formset.save()) and form.is_empty():
                self.object.delete()
                logger.info("empty %s module for page %s by user %s not added",
                            self.object.type, self.object.page.id,
                            self.request.user.username,)
            return redirect_url
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModuleUpdateView(UserPassesTestMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.object.page
        context['form_context'] = "update"
        return context

    def get_success_url(self):
        page_id = self.object.page.id
        return reverse("pages:addmodule", args=[page_id, ])

    def test_func(self):
        page = self.get_object().page
        return self.request.user == page.user


class FormsetModuleUpdateView(ModuleUpdateView):
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
                                                          self.request.FILES,
                                                          instance=self.object)
            else:
                context[self.formset_name] = self.formset(self.request.POST,
                                                          instance=self.object)
        else:
            context[self.formset_name] = self.formset(instance=self.object)
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


class ModuleDeleteView(UserPassesTestMixin, DeleteView):
    template_name = "pages/deletemodule.html"

    def get_success_url(self):
        page_id = self.object.page.id
        return reverse("pages:addmodule", args=[page_id, ])

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        logger.info("user %s deleted object %s from page %s",
                    self.request.user.username,
                    self.object.type, self.object.page.id,
                    )
        success_url = self.get_success_url()
        self.object.page.module_deleted(self.object.position)
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def test_func(self):
        page = self.get_object().page
        return self.request.user == page.user


class GeneralInfoModuleCreateView(ModuleCreateView):
    model = GeneralInfoModule
    form_class = GeneralInfoModuleForm
    template_name = "pages/creategeneralinfomodule.html"


class GeneralInfoModuleUpdateView(ModuleUpdateView):
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


class CommunicationModuleUpdateView(FormsetModuleUpdateView):
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


class DoDontModuleUpdateView(ModuleUpdateView):
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
            logger.info("user %s added item to medicationmodule for page %s",
                        self.request.user.username,
                        self.object.module.page.id)
            if (not formset.save()) and form.is_empty():
                self.object.delete()
                if "submit_add_more" not in self.request.POST and \
                        not self.module.medicationitem_set.exists():
                    self.module.delete()
            # redirect
            if "submit_add_more" in self.request.POST:
                url = reverse("pages:createmoremedicationmodule",
                              args=[self.page.id, self.module.id])
            else:
                url = reverse("pages:addmodule", args=[self.page.id, ])
            return HttpResponseRedirect(url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class MedicationModuleDetailView(UserPassesTestMixin, DetailView):
    model = MedicationModule
    template_name = "pages/medicationmoduledetail.html"

    def test_func(self):
        page = self.get_object().page
        return self.request.user == page.user


class MedicationModuleUpdateView(UserPassesTestMixin, UpdateView):
    model = MedicationItem
    form_class = MedicationItemForm
    template_name = "pages/createmedicationmodule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.module = self.object.module
        context['module'] = self.module
        context['page'] = self.module.page
        context['form_context'] = "update"
        if self.request.POST:
            context['intake_formset'] = IntakeFormSet(self.request.POST,
                                                      instance=self.object)
        else:
            context['intake_formset'] = IntakeFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['intake_formset']
        if formset.is_valid():
            self.object = form.save()
            # save intakes
            formset.instance = self.object
            if (not formset.save()) and form.is_empty():
                self.object.delete()
            # redirect
            url = reverse("pages:medicationmoduledetail",
                          args=[self.module.id, ])
            return HttpResponseRedirect(url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        page = self.get_object().module.page
        return self.request.user == page.user


class MedicationItemDeleteView(UserPassesTestMixin, DeleteView):
    model = MedicationItem
    template_name = "pages/deletemedicationitem.html"

    def get_success_url(self):
        module_id = self.object.module.id
        return reverse("pages:medicationmoduledetail", args=[module_id, ])

    def test_func(self):
        page = self.get_object().module.page
        return self.request.user == page.user


class MedicationModuleDeleteView(ModuleDeleteView):
    model = MedicationModule


class ContactModuleCreateView(FormsetModuleCreateView):
    model = ContactModule
    form_class = ContactModuleForm
    template_name = "pages/createcontactmodule.html"
    formset_name = "contact_formset"
    formset = ContactFormSet


class ContactModuleUpdateView(FormsetModuleUpdateView):
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


class SensoryModuleUpdateView(ModuleUpdateView):
    model = SensoryModule
    form_class = SensoryModuleForm
    template_name = "pages/createsensorymodule.html"


class SensoryModuleDeleteView(ModuleDeleteView):
    model = SensoryModule


class FreeTextModuleCreateView(ModuleCreateView):
    model = FreeTextModule
    form_class = FreeTextModuleForm
    template_name = "pages/createfreetextmodule.html"


class FreeTextModuleUpdateView(ModuleUpdateView):
    model = FreeTextModule
    form_class = FreeTextModuleForm
    template_name = "pages/createfreetextmodule.html"


class FreeTextModuleDeleteView(ModuleDeleteView):
    model = FreeTextModule


class FreeListModuleCreateView(ModuleCreateView):
    model = FreeListModule
    form_class = FreeListModuleForm
    template_name = "pages/createfreelistmodule.html"


class FreeListModuleUpdateView(ModuleUpdateView):
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


class FreePictureModuleUpdateView(FormsetModuleUpdateView):
    model = FreePictureModule
    template_name = "pages/createfreepicturemodule.html"
    form_class = FreePictureModuleForm
    formset_name = "picture_formset"
    formset = PictureFormSet


class FreePictureModuleDeleteView(ModuleDeleteView):
    model = FreePictureModule


class ModuleSortView(UserPassesTestMixin, UpdateView):
    model = Page
    template_name = "pages/sortmodules.html"
    form_class = ModuleSortForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.object.get_all_modules_sorted()
        return context

    def form_valid(self, form):
        if form.has_changed():
            for index, module in \
                    enumerate(self.object.get_all_modules_sorted()):
                new_position = form.cleaned_data.get(
                    "position_{}".format(index + 1))
                if new_position is not module.position:
                    logger.info("Changing position of module %s (%s) "
                                "in page %s from %s to %s",
                                module.type, module.id, self.object.id,
                                module.position, new_position)
                    module.position = new_position
                    module.save()
        page_id = self.object.id
        return HttpResponseRedirect(
            reverse("pages:pagepreview", args=[page_id, ]))

    def test_func(self):
        return self.request.user == self.get_object().user


class PagePreview(UserPassesTestMixin, DetailView):
    model = Page
    template_name = "pages/page_preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.object.get_all_modules_sorted()
        return context

    def test_func(self):
        return self.request.user == self.get_object().user


class PageListView(LoginRequiredMixin, ListView):
    model = Page
    template_name = "pages/page_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user,
                                             is_active=True)


class PageVisibilityView(UserPassesTestMixin, UpdateView):
    model = Page
    http_method_names = ['post']
    fields = []

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_visible:
            self.object.is_visible = False
            logger.info("user %s changed page %s visibility to private",
                        self.request.user.username, self.object.id)
        else:
            self.object.is_visible = True
            logger.info("user %s changed page %s visibility to visible",
                        self.request.user.username, self.object.id)
            # Todo: create token if no token exists
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("pages:pagelist")

    def test_func(self):
        return self.request.user == self.get_object().user


class PageTokenGenerationView(UserPassesTestMixin, UpdateView):
    model = Page
    http_method_names = ['post']
    fields = []

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        token = self.object.make_token()
        logger.info("user %s generated token %s for page %s ",
                    self.request.user.username,
                    token, self.object.id)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("pages:pagelist")

    def test_func(self):
        return self.request.user == self.get_object().user


class ViewPageTokenView(DetailView):
    model = Page
    template_name = "pages/page_view.html"

    def get_object(self, queryset=None):
        uidb64 = self.kwargs.get("uidb64")
        token = self.kwargs.get("token")
        page_id = force_text(urlsafe_base64_decode(uidb64))
        page = Page.objects.active().get(pk=page_id)
        if page.check_token(token):
            logger.info("Valid token link used for page %s", page_id)
            return page
        else:
            logger.info("Invalid token link used for page %s", page_id)
            raise Http404(_("No Page found matching the query"))
