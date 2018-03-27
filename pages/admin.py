from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from .models import FreeTextModule, GeneralInfoModule, Page, FreeListModule,\
                    CommunicationModule, FreePictureModule, \
                    ModulePicture, DoDontModule, SensoryModule, \
                    CommunicationMethods, ContactModule, ModuleContact, \
                    MedicationModule, MedicationItem, MedicationIntake

# Register your models here.
admin.site.register(GeneralInfoModule)
admin.site.register(SensoryModule)
admin.site.register(DoDontModule)
admin.site.register(FreeTextModule)
admin.site.register(FreeListModule)


class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.model_name),
                      args=[instance.pk])
        if instance.pk:
            return mark_safe(u'<a href="{u}">edit</a>'.format(u=url))
        else:
            return ''


class GeneralInfoModuleInline(admin.TabularInline):
    model = GeneralInfoModule
    extra = 0


class SensoryModuleInline(admin.TabularInline):
    model = SensoryModule
    extra = 0


class FreeTextModuleInline(admin.TabularInline):
    model = FreeTextModule
    extra = 0


class FreeListModuleInline(admin.TabularInline):
    model = FreeListModule
    extra = 0


class DoDontModuleInline(admin.TabularInline):
    model = DoDontModule
    extra = 0


class MedicationModuleInline(EditLinkToInlineObject, admin.TabularInline):
    model = MedicationModule
    readonly_fields = ('edit_link', )
    extra = 0


class CommunicationModuleInline(EditLinkToInlineObject, admin.TabularInline):
    model = CommunicationModule
    readonly_fields = ('edit_link', )
    extra = 0


class ContactModuleInline(EditLinkToInlineObject, admin.TabularInline):
    model = ContactModule
    readonly_fields = ('edit_link', )
    extra = 0


class FreePictureModuleInline(EditLinkToInlineObject, admin.TabularInline):
    model = FreePictureModule
    readonly_fields = ('edit_link', )
    extra = 0


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'module_num', 'created_at']
    inlines = [
        GeneralInfoModuleInline,
        SensoryModuleInline,
        DoDontModuleInline,
        FreeListModuleInline,
        FreeTextModuleInline,
        MedicationModuleInline,
        CommunicationModuleInline,
        ContactModuleInline,
        FreePictureModuleInline
    ]


class PictureInline(admin.TabularInline):
    model = ModulePicture
    extra = 0


@admin.register(FreePictureModule)
class FreePictureAdmin(admin.ModelAdmin):
    inlines = [
        PictureInline,
    ]


class CommInline(admin.TabularInline):
    model = CommunicationMethods
    extra = 0


@admin.register(CommunicationModule)
class CommAdmin(admin.ModelAdmin):
    inlines = [
        CommInline,
    ]


class ContactInline(admin.TabularInline):
    model = ModuleContact
    extra = 0


@admin.register(ContactModule)
class ContactAdmin(admin.ModelAdmin):
    inlines = [
        ContactInline,
    ]


class MedItemInline(EditLinkToInlineObject, admin.TabularInline):
    model = MedicationItem
    readonly_fields = ('edit_link', )
    extra = 0


@admin.register(MedicationModule)
class MedicationAdmin(admin.ModelAdmin):
    inlines = [MedItemInline, ]


class MedIntakeInline(admin.TabularInline):
    model = MedicationIntake
    extra = 0


@admin.register(MedicationItem)
class MedItemAdmin(admin.ModelAdmin):
    inlines = [
        MedIntakeInline,
    ]
