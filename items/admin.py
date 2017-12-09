from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 0

class ItemCategoryAdmin (admin.ModelAdmin):

    list_display = [field.name for field in ItemCategory._meta.fields]

    class Meta:
        model = ItemCategory

admin.site.register(ItemCategory, ItemCategoryAdmin)

class ItemManufacturerAdmin (admin.ModelAdmin):

    list_display = [field.name for field in ItemManufacturer._meta.fields]

    class Meta:
        model = ItemManufacturer

admin.site.register(ItemManufacturer, ItemManufacturerAdmin)

class ItemAdmin (ImportExportModelAdmin): #Для импорта-экспорта используется скаченная библиотека django-import-export

    list_display = [field.name for field in Item._meta.fields]
    inlines = [ItemImageInline]
    list_filter = ['category', 'manufacturer', 'power']
    search_fields = ['vendor_code', 'power']

    class Meta:
        model = Item

admin.site.register(Item, ItemAdmin)

class ItemImageAdmin (admin.ModelAdmin):

    list_display = [field.name for field in ItemImage._meta.fields]


    class Meta:
        model = ItemImage

admin.site.register(ItemImage, ItemImageAdmin)