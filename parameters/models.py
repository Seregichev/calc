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

class CategoryAtribute(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Название")
    is_active = models.BooleanField(default=True, verbose_name="Активно?")

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Категория атрибута"
        verbose_name_plural = "Категории атрибутов"

class Atribute(models.Model):
    category = models.ForeignKey(CategoryAtribute, blank=True, null=True, default=None, verbose_name="Категория")
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Название")
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Величина")
    is_active = models.BooleanField(default=True, verbose_name="Активно?")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Обновленно")

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"

class ItemCategoryParameter(models.Model):
    parameter = models.ForeignKey(Parameter, blank=True, null=True, default=None, verbose_name="Тип пуска")
    item_category = models.ForeignKey(ItemCategory, blank=True, null=True, default=None, verbose_name="Категория изделия")
    nmb = models.IntegerField(default=1, verbose_name="Колличество", help_text="Укажите колличество изделий выбранной категории которые должны автоматически добавляться")
    item_paramater_do_more = models.BooleanField(default=False, verbose_name="На ступень выше?", help_text="Отметьте галочкой, если необходимо подбирать изделие на ступень выше")
    is_active = models.BooleanField(default=True, verbose_name="Активно?")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Обновленно")

    def __str__(self):
        return "%s" % (self.item_category)

    class Meta:
        verbose_name = "Категория изделия в параметре"
        verbose_name_plural = "Категории изделий в параметрах"
