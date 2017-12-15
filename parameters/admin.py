from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *


class ParameterInline(admin.TabularInline):
    model = Parameter
    extra = 0

class CategoryParameterAdmin (ImportExportModelAdmin):

    list_display = [field.name for field in CategoryParameter._meta.fields]
    inlines = [ParameterInline]

    class Meta:
        model = CategoryParameter

admin.site.register(CategoryParameter, CategoryParameterAdmin)

class ParameterAdmin (ImportExportModelAdmin): #Для импорта-экспорта используется скаченная библиотека django-import-export

    list_display = [field.name for field in Parameter._meta.fields]
    list_filter = ['category']
    search_fields = ['name']

    class Meta:
        model = Parameter

admin.site.register(Parameter, ParameterAdmin)


class ItemCategoryParameterAdmin (ImportExportModelAdmin): #Для импорта-экспорта используется скаченная библиотека django-import-export

    list_display = [field.name for field in ItemCategoryParameter._meta.fields]

    class Meta:
        model = ItemCategoryParameter

admin.site.register(ItemCategoryParameter, ItemCategoryParameterAdmin)