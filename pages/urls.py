"""Pages app URL Configuration

* Page CRUD
* GeneralInfoModule CRUD
* CommunicationModule CRUD
* DoDontModule CRUD
* MedicationModule CRUD
* SensoryModule CRUD
* ContactModule CRUD
* FreeTextModule CRUD
* FreeListModule CRUD
* FreePictureModule CRUD
* Other page related views:
    - sortmodules
    - PagePreview
    - viewpage (token based pageview)
    - pagevisibility
    - token generation
    - page list
    - page duplication (duplicating examples)
"""

from django.conf.urls import url

from .views import GeneralInfoModuleCreateView, PageCreateView,\
                   FreeTextModuleCreateView, SelectModuleView, PagePreview,\
                   FreeListModuleCreateView, FreePictureModuleCreateView, \
                   CommunicationModuleCreateView, \
                   DoDontModuleCreateView, MedicationModuleCreateView,\
                   ContactModuleCreateView, SensoryModuleCreateView, \
                   GeneralInfoModuleDeleteView, CommunicationModuleDeleteView,\
                   DoDontModuleDeleteView, MedicationModuleDeleteView, \
                   SensoryModuleDeleteView, ContactModuleDeleteView, \
                   FreeTextModuleDeleteView, FreeListModuleDeleteView, \
                   FreePictureModuleDeleteView, GeneralInfoModuleUpdateView, \
                   CommunicationModuleUpdateView, DoDontModuleUpdateView, \
                   SensoryModuleUpdateView, ContactModuleUpdateView, \
                   FreeTextModuleUpdateView, FreeListModuleUpdateView, \
                   FreePictureModuleUpdateView, MedicationModuleUpdateView, \
                   MedicationModuleDetailView, MedicationItemDeleteView, \
                   ModuleSortView, PageListView, PageVisibilityView, \
                   PageTokenGenerationView, ViewPageTokenView, PageDeleteView,\
                   PageDuplicateView

urlpatterns = [
    # Page CRUD
    url(r'^createpage/$', PageCreateView.as_view(), name="createpage"),
    url(r'^(?P<pk>[0-9]+)/addmodule/$',
        SelectModuleView.as_view(), name="addmodule"),
    url(r'^deletepage/(?P<pk>[0-9]+)/$', PageDeleteView.as_view(),
        name="deletepage"),
    # GeneralInfoModule CRUD
    url(r'^(?P<page_id>[0-9]+)/creategeneralinfomodule/$',
        GeneralInfoModuleCreateView.as_view(), name="creategeneralinfomodule"),
    url(r'^editgeneralinfomodule/(?P<pk>[0-9]+)/$',
        GeneralInfoModuleUpdateView.as_view(), name="updategeneralinfomodule"),
    url(r'^deletegeneralinfomodule/(?P<pk>[0-9]+)/$',
        GeneralInfoModuleDeleteView.as_view(), name="deletegeneralinfomodule"),
    # CommunicationModule CRUD
    url(r'^(?P<page_id>[0-9]+)/createcommunicationmodule/$',
        CommunicationModuleCreateView.as_view(),
        name="createcommunicationmodule"),
    url(r'^editcommunicationmodule/(?P<pk>[0-9]+)/$',
        CommunicationModuleUpdateView.as_view(),
        name="updatecommunicationmodule"),
    url(r'^deletecommunicationmodule/(?P<pk>[0-9]+)/$',
        CommunicationModuleDeleteView.as_view(),
        name="deletecommunicationmodule"),
    # DoDontModule CRUD
    url(r'^(?P<page_id>[0-9]+)/createdodontmodule/$',
        DoDontModuleCreateView.as_view(), name="createdodontmodule"),
    url(r'^editdodontmodule/(?P<pk>[0-9]+)/$',
        DoDontModuleUpdateView.as_view(), name="updatedodontmodule"),
    url(r'^deletedodontmodule/(?P<pk>[0-9]+)/$',
        DoDontModuleDeleteView.as_view(), name="deletedodontmodule"),
    # MedicationModule CRUD
    url(r'^(?P<page_id>[0-9]+)/createmedicationmodule/(?P<module_id>[0-9]+)/$',
        MedicationModuleCreateView.as_view(),
        name="createmoremedicationmodule"),
    url(r'^(?P<page_id>[0-9]+)/createmedicationmodule/$',
        MedicationModuleCreateView.as_view(), name="createmedicationmodule"),
    url(r'^medicationmodule/(?P<pk>[0-9]+)/$',
        MedicationModuleDetailView.as_view(), name="medicationmoduledetail"),
    url(r'^editmedicationmodule/(?P<pk>[0-9]+)/$',
        MedicationModuleUpdateView.as_view(), name="updatemedicationmodule"),
    url(r'^deletemedicationitem/(?P<pk>[0-9]+)/$',
        MedicationItemDeleteView.as_view(), name="deletemedicationitem"),
    url(r'^deletemedicationmodule/(?P<pk>[0-9]+)/$',
        MedicationModuleDeleteView.as_view(), name="deletemedicationmodule"),
    # SensoryModule CRUD
    url(r'^(?P<page_id>[0-9]+)/createsensorymodule/$',
        SensoryModuleCreateView.as_view(), name="createsensorymodule"),
    url(r'^editsensorymodule/(?P<pk>[0-9]+)/$',
        SensoryModuleUpdateView.as_view(), name="updatesensorymodule"),
    url(r'^deletesensorymodule/(?P<pk>[0-9]+)/$',
        SensoryModuleDeleteView.as_view(), name="deletesensorymodule"),
    # ContactModule CRUD
    url(r'^(?P<page_id>[0-9]+)/createcontactmodule/$',
        ContactModuleCreateView.as_view(), name="createcontactmodule"),
    url(r'^editcontactmodule/(?P<pk>[0-9]+)/$',
        ContactModuleUpdateView.as_view(), name="updatecontactmodule"),
    url(r'^deletecontactmodule/(?P<pk>[0-9]+)/$',
        ContactModuleDeleteView.as_view(), name="deletecontactmodule"),
    # FreeTextModule CRUD
    url(r'^(?P<page_id>[0-9]+)/createfreetextmodule/$',
        FreeTextModuleCreateView.as_view(), name="createfreetextmodule"),
    url(r'^editfreetextmodule/(?P<pk>[0-9]+)/$',
        FreeTextModuleUpdateView.as_view(), name="updatefreetextmodule"),
    url(r'^deletefreetextmodule/(?P<pk>[0-9]+)/$',
        FreeTextModuleDeleteView.as_view(), name="deletefreetextmodule"),
    # FreeListModule CRUD
    url(r'^(?P<page_id>[0-9]+)/createfreelistmodule/$',
        FreeListModuleCreateView.as_view(), name="createfreelistmodule"),
    url(r'^editfreelistmodule/(?P<pk>[0-9]+)/$',
        FreeListModuleUpdateView.as_view(), name="updatefreelistmodule"),
    url(r'^deletefreelistmodule/(?P<pk>[0-9]+)/$',
        FreeListModuleDeleteView.as_view(), name="deletefreelistmodule"),
    # FreePictureModule CRUD
    url(r'^(?P<page_id>[0-9]+)/createfreepicturemodule/$',
        FreePictureModuleCreateView.as_view(), name="createfreepicturemodule"),
    url(r'^editfreepicturemodule/(?P<pk>[0-9]+)/$',
        FreePictureModuleUpdateView.as_view(), name="updatefreepicturemodule"),
    url(r'^deletefreepicturemodule/(?P<pk>[0-9]+)/$',
        FreePictureModuleDeleteView.as_view(), name="deletefreepicturemodule"),
    # Other views
    url(r'^(?P<pk>[0-9]+)/sortmodules/$', ModuleSortView.as_view(),
        name="sortmodules"),
    url(r'^(?P<pk>[0-9]+)/preview/(?P<reason>creating|final|admin)/$',
        PagePreview.as_view(), name="pagepreview"),
    url(r'^viewpage/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        '(?P<token>[0-9A-Za-z]{1,20})/$',
        ViewPageTokenView.as_view(), name="viewpage"),
    url(r'^(?P<pk>[0-9]+)/visibility/$',
        PageVisibilityView.as_view(), name="pagevisibility"),
    url(r'^(?P<pk>[0-9]+)/generatetoken/$',
        PageTokenGenerationView.as_view(), name="pagegeneratetoken"),
    url(r'^mypages/$', PageListView.as_view(), name="pagelist"),
    url(r'^(?P<pk>[0-9]+)/duplicatepage/$',
        PageDuplicateView.as_view(), name="duplicatepage"),
]
