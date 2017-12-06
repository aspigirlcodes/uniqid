from django.views.generic import CreateView, DetailView, UpdateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import Page, GeneralInfoModule, FreeTextModule, FreeListModule,\
                    CommunicationMethodsModule, FreePictureModule, DoDontModule
from .forms import PageCreateForm, GeneralInfoModuleForm, AddModuleForm,\
                   FreeTextModuleForm, FreeListModuleForm,\
                   CommunicationMethodsModuleForm, PictureFormSet, \
                   DoDontModuleForm


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
        self.object = form.save(commit=False)
        self.object.page = self.page
        self.object.position = self.page.module_num + 1
        self.object.save()
        self.page.module_num += 1
        self.page.save()
        url = reverse("pages:addmodule", args=[self.page.id, ])
        return HttpResponseRedirect(url)


class GeneralInfoModuleCreateView(ModuleCreateView):
    model = GeneralInfoModule
    form_class = GeneralInfoModuleForm
    template_name = "pages/creategeneralinfomodule.html"


class CommunicationMethodsModuleCreateView(ModuleCreateView):
    model = CommunicationMethodsModule
    form_class = CommunicationMethodsModuleForm
    template_name = "pages/createcommunicationmethodsmodule.html"


class DoDontModuleCreateView(ModuleCreateView):
    model = DoDontModule
    form_class = DoDontModuleForm
    template_name = "pages/createdodontmodule.html"


class FreeTextModuleCreateView(ModuleCreateView):
    model = FreeTextModule
    form_class = FreeTextModuleForm
    template_name = "pages/createfreetextmodule.html"


class FreeListModuleCreateView(ModuleCreateView):
    model = FreeListModule
    form_class = FreeListModuleForm
    template_name = "pages/createfreelistmodule.html"


class FreePictureModuleCreateView(ModuleCreateView):
    model = FreePictureModule
    template_name = "pages/createfreepicturemodule.html"
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['picture_formset'] = PictureFormSet(self.request.POST,
                                                        self.request.FILES)
        else:
            context['picture_formset'] = PictureFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['picture_formset']
        if formset.is_valid():
            redirect_url = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return redirect_url
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PagePreview(DetailView):
    model = Page
    template_name = "pages/page_preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.object.get_all_modules_sorted()
        return context
