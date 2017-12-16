from django import forms
from items.models import Item
from parameters.models import Parameter, CategoryParameter



class AddPowerForm (forms.Form):
    comment = forms.CharField(required=True,widget=forms.TextInput(
                                attrs={'placeholder': 'Примечание','class':'form-control'}
                                ))

    voltage = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True).values_list('voltage', flat=True)
                               .order_by('voltage').distinct(), empty_label="Напряжение")
    power = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True).values_list('power', flat=True)
                                   .order_by('power').distinct(), empty_label="Мощность")
    parameter = forms.ModelChoiceField(queryset=Parameter.objects.filter(
                        category=CategoryParameter.objects.filter(name='Способ пуска',is_active=True),
                        is_active=True),
                  empty_label="Способ пуска")
