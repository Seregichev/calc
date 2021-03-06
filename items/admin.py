from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

# класс выводит изображения изделия внизу карточки товара
class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 0

# класс выводит дополнительные изделия внизу карточки товара
class AddItemInline(admin.TabularInline):
    model = AddItem
    fk_name = 'main_item'
    can_delete = False
    extra = 0

    # фильтруем выпадающий список поля доп. изделия по серии редактируемого изделия
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "adding_item":
            gotten_id = ''
            # из адреса request выбираем только id изделия
            for e in request.path_info.split('/'):
                if e.isdigit():
                    gotten_id = e
            # по полученному id изделия находим его серию и отфильтровываем выпадающий список изделий по серии

            kwargs["queryset"] = Item.objects.filter(series=Item.objects.filter(id=gotten_id or None, is_active=True)
                                                     .values('series'),is_active=True)
        return super(AddItemInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

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

class ItemAdminResource(resources.ModelResource):
    category = fields.Field(column_name='category', attribute='category', widget=ForeignKeyWidget(ItemCategory, 'name'))
    manufacturer = fields.Field(column_name='manufacturer', attribute='manufacturer', widget=ForeignKeyWidget(ItemManufacturer, 'name'))

    class Meta:
        model = Item

class ItemAdmin (ImportExportModelAdmin): #Для импорта-экспорта используется скаченная библиотека django-import-export

    # list_display = [field.name for field in Item._meta.fields]
    list_display = ('id', 'category', 'vendor_code', 'name', 'manufacturer', 'series', 'voltage', 'power', 'is_active',
                    'price', 'currency', 'created', 'updated')
    list_display_links = ('id', 'name', 'vendor_code')
    list_editable = ('is_active', 'price', 'currency')
    inlines = [AddItemInline, ItemImageInline]
    list_filter = ['category', 'manufacturer', 'power']
    search_fields = ['vendor_code', 'power']

    resource_class = ItemAdminResource

admin.site.register(Item, ItemAdmin)

class ItemImageAdmin (admin.ModelAdmin):

    list_display = [field.name for field in ItemImage._meta.fields]


    class Meta:
        model = ItemImage

admin.site.register(ItemImage, ItemImageAdmin)

class AddItemAdmin (ImportExportModelAdmin):

    list_display = [field.name for field in AddItem._meta.fields]

    class Meta:
        model = AddItem

admin.site.register(AddItem, AddItemAdmin)