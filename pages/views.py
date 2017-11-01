from django.views.generic import CreateView, DetailView, UpdateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import Page, GeneralInfoModule, FreeTextModule
from .forms import PageCreateForm, GeneralInfoModuleForm, AddModuleForm


class PageCreateView(CreateView):
    model = Page
    form_class = PageCreateForm
    template_name = "pages/createpage.html"

    def form_valid(self, form):
        self.object = form.save()
        url_name = "pages:create" + form.cleaned_data['module']
        url = reverse(url_name, args=[self.object.id, ])
        return HttpResponseRedirect(url)


class GeneralInfoModuleCreateView(CreateView):
    model = GeneralInfoModule
    form_class = GeneralInfoModuleForm
    template_name = "pages/creategeneralinfomodule.html"

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


class FreeTextModuleCreateView(CreateView):
    model = FreeTextModule
    template_name = "pages/empty.html"
    fields = []


class SelectModuleView(UpdateView):
    model = Page
    form_class = AddModuleForm
    template_name = "pages/createpage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.object.get_all_modules()
        print(context['modules'])
        return context

    def form_valid(self, form):
        self.object = form.save()
        url_name = "pages:create" + form.cleaned_data['module']
        url = reverse(url_name, args=[self.object.id, ])
        return HttpResponseRedirect(url)


class PagePreview(DetailView):
    model = Page
    template_name = "pages/empty.html"
