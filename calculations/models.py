from django.db import models
from items.models import Item
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Calculate(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    calculate_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # total price in calculate
    comments = models.TextField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Расчет %s : %s" % (self.id,self.calculate_name)

    class Meta:
        verbose_name = "Расчет"
        verbose_name_plural = "Расчеты"

    def save(self, *args, **kwargs):
        super(Calculate, self).save(*args, **kwargs)

class ItemInCalculate(models.Model):
    calculate = models.ForeignKey(Calculate, blank=True, null=True, default=None, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, blank=True, null=True, default=None, on_delete=models.CASCADE)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0) #price_per_item * nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.item.name

    class Meta:
        verbose_name = "Изделие в расчете"
        verbose_name_plural = "Изделие в расчете"

    def save(self, *args, **kwargs):
        price_per_item = self.item.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * self.price_per_item

        super(ItemInCalculate, self).save(*args, **kwargs)

class ItemInEstimate(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    uuid_id = models.UUIDField(blank=False, null=True, default=None)
    comment = models.CharField(max_length=128, blank=True, null=True, default=None)
    item = models.ForeignKey(Item, blank=True, null=True, default=None, on_delete=models.CASCADE)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0) #price_per_item * nmb
    is_active = models.BooleanField(default=True)
    calculate = models.ForeignKey(Calculate, blank=True, null=True, default=None, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.item.name

    class Meta:
        verbose_name = "Изделие в смете"
        verbose_name_plural = "Изделия в смете"

    def save(self, *args, **kwargs):
        price_per_item = self.item.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * self.price_per_item

        super(ItemInEstimate, self).save(*args, **kwargs)

def item_in_calculate_post_save(sender,instance,created,**kwargs):
    calculate = instance.calculate
    all_item_in_calculate = ItemInCalculate.objects.filter(calculate=calculate, is_active=True)

    calculate_total_price = 0
    for item in all_item_in_calculate:
        calculate_total_price += item.total_price

    instance.calculate.total_price = calculate_total_price
    instance.calculate.save(force_update=True)

post_save.connect(item_in_calculate_post_save, sender=ItemInCalculate)