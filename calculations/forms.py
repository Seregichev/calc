from django import forms
from items.models import Item



class AddPowerForm (forms.Form):
    voltage = forms.ModelChoiceField(required=True, queryset=Item.objects.filter(is_active=True).values_list('voltage', flat=True)
                               .order_by('voltage').distinct(), empty_label="Напряжение")
    power = forms.ModelChoiceField(required=True, queryset=Item.objects.filter(is_active=True).values_list('power', flat=True)
                                   .order_by('power').distinct(), empty_label="Мощность")
