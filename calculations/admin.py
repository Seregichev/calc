from django.contrib import admin
from .models import Calculate, ItemInCalculate

class ItemInCalculateInline(admin.TabularInline):
    model = ItemInCalculate
    extra = 0

class CalculateAdmin (admin.ModelAdmin):

    list_display = [field.name for field in Calculate._meta.fields]
    inlines = [ItemInCalculateInline]

    class Meta:
        model = Calculate

admin.site.register(Calculate, CalculateAdmin)

class ItemInCalculateAdmin (admin.ModelAdmin):

    list_display = [field.name for field in ItemInCalculate._meta.fields]

    class Meta:
        model= ItemInCalculate

admin.site.register(ItemInCalculate, ItemInCalculateAdmin)