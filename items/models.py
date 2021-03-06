from django.db import models

TYPE_CURRENT_CHOICES = (
    ('AC','AC'),
    ('DC','DC')
)
TYPE_PROTECT_CLASS = (
    ('10','10'),
    ('20','20'),
    ('30','30'),
    ('40','40'),
)

class ItemCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Название")
    is_active = models.BooleanField(default=True, verbose_name="Активно?")

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Категория изделия"
        verbose_name_plural = "Категории изделий"

class ItemManufacturer(models.Model):
    short_name = models.CharField(max_length=5, blank=True, null=True, default=None, verbose_name="Сокращение")
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Название")
    is_active = models.BooleanField(default=True, verbose_name="Активно?")

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Производитель изделия"
        verbose_name_plural = "Производители изделий"

class Item(models.Model):
    category = models.ForeignKey(ItemCategory, blank=True, null=True, default=None, verbose_name="Категория",
                                 on_delete=models.DO_NOTHING)
    manufacturer = models.ForeignKey(ItemManufacturer, blank=True, null=True, default=None,
                                     verbose_name="Производитель", on_delete=models.DO_NOTHING)
    series = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Серия")
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Название")
    vendor_code = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Артикул")
    description = models.TextField(blank=True, null=True, default=None, verbose_name="Описание")

    voltage = models.DecimalField(max_digits=7, decimal_places=0, default=0, verbose_name="Напряжение [В]")
    current = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="Ток [А]")
    type_current = models.CharField(choices=TYPE_CURRENT_CHOICES, max_length=3, blank=True, null=True, default='AC',
                                    verbose_name="Вид тока")
    power = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="Мощность [кВт]")
    protect_class = models.CharField(choices=TYPE_PROTECT_CLASS, max_length=3, blank=True, null=True, default=None,
                                    verbose_name="Класс тепловой защиты")

    force_input = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name="Силовые входы [шт]")

    discret_input = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name="Дискретные входы [шт]")
    discret_output = models.DecimalField(max_digits=4, decimal_places=0, default=0,
                                         verbose_name="Дискретные выходы [шт]")
    analog_input = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name="Аналоговые входы [шт]")
    analog_output = models.DecimalField(max_digits=4, decimal_places=0, default=0,
                                        verbose_name="Аналоговые выходы [шт]")
    temperature_input = models.DecimalField(max_digits=4, decimal_places=0, default=0,
                                            verbose_name="Температурные входы [шт]")

    height = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Высота")
    width = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ширина")
    depth = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Глубина")
    area = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Площадь")


    atributes = models.ManyToManyField('parameters.Atribute', blank=True, default=None, verbose_name="Атрибуты изделия")

    is_active = models.BooleanField(default=True, verbose_name="Активно?")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")
    currency = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Валюта")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Обновленно")

    def __str__(self):
        return "%s, %s" % (self.vendor_code, self.name)

    class Meta:
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия"

    def save(self, *args, **kwargs):
        if self.height > 0 and self.width and self.area == 0:
            self.area = self.height * self.width
        super(Item, self).save(*args, **kwargs)

class ItemImage(models.Model):
    item = models.ForeignKey(Item, blank=True, null=True, default=None, verbose_name="Изделие",
                             on_delete=models.DO_NOTHING)
    image = models.ImageField (upload_to='items_images/', verbose_name="Изображение")
    is_main = models.BooleanField(default=False, verbose_name="Основное?")
    is_active = models.BooleanField(default=True, verbose_name="Активно?")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Обновленно")

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

# Клас дополнительных изделий, нужен для подбора дополнительных изделий обязательных и необязательных
class AddItem(models.Model):
    main_item = models.ForeignKey(Item, blank=True, null=True, default=None, verbose_name="Основное изделие",
                                  related_name="main_item", on_delete=models.DO_NOTHING)
    adding_item = models.ForeignKey(Item, blank=True, null=True, default=None, verbose_name="Дополнительное изделие",
                                    related_name="adding_item", on_delete=models.DO_NOTHING)
    required = models.BooleanField(default=False, verbose_name="Обязательное устройство",
                                   help_text="Отметьте галочкой, если необходимо обязательно добавить изделие")
    nmb = models.IntegerField(default=1, verbose_name="Колличество",
                              help_text="Укажите колличество выбранных дополнительных изделий которые должны автоматически добавляться")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Обновленно")

    def __str__(self):
        return "%s" % (self.adding_item)

    class Meta:
        unique_together = ("main_item", "adding_item")
        verbose_name = "Дополнительное изделие"
        verbose_name_plural = "Дополнительные изделия"
