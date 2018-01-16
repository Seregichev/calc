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

class ItemCategoryParameterInline(admin.TabularInline):
    model = ItemCategoryParameter
    extra = 0

class ParameterAdmin (ImportExportModelAdmin): #Для импорта-экспорта используется скаченная библиотека django-import-export

    list_display = [field.name for field in Parameter._meta.fields]
    list_filter = ['category']
    search_fields = ['name']
    inlines = [ItemCategoryParameterInline]

    class Meta:
        model = Parameter

admin.site.register(Parameter, ParameterAdmin)


class ItemCategoryParameterAdmin (ImportExportModelAdmin): #Для импорта-экспорта используется скаченная библиотека django-import-export

    list_display = [field.name for field in ItemCategoryParameter._meta.fields]
    list_filter = ['parameter']

    class Meta:
        model = ItemCategoryParameter

admin.site.register(ItemCategoryParameter, ItemCategoryParameterAdmin)

class AtributeInline(admin.TabularInline):
    model = Atribute
    extra = 0

class CategoryAtributeAdmin (ImportExportModelAdmin):

    list_display = [field.name for field in CategoryAtribute._meta.fields]
    inlines = [AtributeInline]

    class Meta:
        model = CategoryAtribute

admin.site.register(CategoryAtribute, CategoryAtributeAdmin)

class AtributeAdmin (ImportExportModelAdmin): #Для импорта-экспорта используется скаченная библиотека django-import-export

    list_display = [field.name for field in Atribute._meta.fields]
    list_filter = ['category']
    search_fields = ['name']

    class Meta:
        model = Atribute

admin.site.register(Atribute, AtributeAdmin)