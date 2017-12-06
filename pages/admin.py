from django.contrib import admin
from .models import FreeTextModule, GeneralInfoModule, Page, FreeListModule,\
                    CommunicationMethodsModule, FreePictureModule, \
                    ModulePicture

# Register your models here.
admin.site.register(Page)
admin.site.register(GeneralInfoModule)
admin.site.register(CommunicationMethodsModule)
admin.site.register(FreeTextModule)
admin.site.register(FreeListModule)


class PictureInline(admin.TabularInline):
    model = ModulePicture
    extra = 0


@admin.register(FreePictureModule)
class FreePictureAdmin(admin.ModelAdmin):
    inlines = [
        PictureInline,
    ]
