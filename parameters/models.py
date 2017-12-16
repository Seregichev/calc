from django.db import models
from items.models import ItemCategory



class CategoryParameter(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Название")
    is_active = models.BooleanField(default=True, verbose_name="Активно?")

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Категория параметра"
        verbose_name_plural = "Категории параметров"

class Parameter(models.Model):
    category = models.ForeignKey(CategoryParameter, blank=True, null=True, default=None, verbose_name="Категория")
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Название")
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Величина")
    is_active = models.BooleanField(default=True, verbose_name="Активно?")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Обновленно")

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"

class ItemCategoryParameter(models.Model):
    parameter = models.ForeignKey(Parameter, blank=True, null=True, default=None, verbose_name="Тип пуска")
    item_category = models.ForeignKey(ItemCategory, blank=True, null=True, default=None, verbose_name="Категория изделия")
    nmb = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True, verbose_name="Активно?")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Обновленно")

    def __str__(self):
        return "%s" % (self.item_category)

    class Meta:
        verbose_name = "Категория изделия в параметре"
        verbose_name_plural = "Категории изделий в параметрах"


# class ItemManufacturer(models.Model):
#     short_name = models.CharField(max_length=5, blank=True, null=True, default=None, verbose_name="Сокращение")
#     name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Название")
#     is_active = models.BooleanField(default=True, verbose_name="Активно?")
#
#     def __str__(self):
#         return "%s" % (self.name)
#
#     class Meta:
#         verbose_name = "Производитель изделия"
#         verbose_name_plural = "Производители изделий"
#
#
# class Item(models.Model):
#     category = models.ForeignKey(ItemCategory, blank=True, null=True, default=None, verbose_name="Категория")
#     manufacturer = models.ForeignKey(ItemManufacturer, blank=True, null=True, default=None,
#                                      verbose_name="Производитель")
#     series = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Серия")
#     name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Название")
#     vendor_code = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Артикул")
#     description = models.TextField(blank=True, null=True, default=None, verbose_name="Описание")
#
#
#     voltage = models.DecimalField(max_digits=7, decimal_places=0, default=0, verbose_name="Напряжение [В]")
#     power = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="Мощность [кВт]")
#
#     force_input = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name="Силовые входы [шт]")
#
#     discret_input = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name="Дискретные входы [шт]")
#     discret_output = models.DecimalField(max_digits=4, decimal_places=0, default=0,
#                                          verbose_name="Дискретные выходы [шт]")
#     analog_input = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name="Аналоговые входы [шт]")
#     analog_output = models.DecimalField(max_digits=4, decimal_places=0, default=0,
#                                         verbose_name="Аналоговые выходы [шт]")
#     temperature_input = models.DecimalField(max_digits=4, decimal_places=0, default=0,
#                                             verbose_name="Температурные входы [шт]")
#
#     profinet = models.BooleanField(default=False, verbose_name="ProfiNET")
#     profibus = models.BooleanField(default=False, verbose_name="ProfiBus")
#     ethernet = models.BooleanField(default=False, verbose_name="EtherNET")
#     rs484 = models.BooleanField(default=False, verbose_name="RS484")
#
#     height = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Высота")
#     width = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ширина")
#     depth = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Глубина")
#
#     is_active = models.BooleanField(default=True, verbose_name="Активно?")
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")
#     currency = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Валюта")
#     created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
#     updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Обновленно")
#
#     def __str__(self):
#         return "%s, %s" % (self.name, self.price)
#
#     class Meta:
#         verbose_name = "Изделие"
#         verbose_name_plural = "Изделия"
#
# class ItemImage(models.Model):
#     item = models.ForeignKey(Item, blank=True, null=True, default=None, verbose_name="Изделие")
#     image = models.ImageField (upload_to='items_images/', verbose_name="Изображение")
#     is_main = models.BooleanField(default=False, verbose_name="Основное?")
#     is_active = models.BooleanField(default=True, verbose_name="Активно?")
#     created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
#     updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Обновленно")
#
#     def __str__(self):
#         return "%s" % (self.id,)
#
#     class Meta:
#         verbose_name = "Изображение"
#         verbose_name_plural = "Изображения"
