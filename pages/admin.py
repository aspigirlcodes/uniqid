from django.contrib import admin
from .models import FreeTextModule, GeneralInfoModule, Page, FreeListModule,\
                    CommunicationMethodsModule

# Register your models here.
admin.site.register(Page)
admin.site.register(GeneralInfoModule)
admin.site.register(CommunicationMethodsModule)
admin.site.register(FreeTextModule)
admin.site.register(FreeListModule)
