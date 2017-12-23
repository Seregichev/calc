from django import forms
from items.models import Item
from parameters.models import Parameter, CategoryParameter, Atribute, CategoryAtribute



class AddPowerForm (forms.Form):
    comment = forms.CharField(required=True,  widget=forms.TextInput(
                                attrs={'placeholder': u'Назначение','class':'form-control'})
                              )

    voltage = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True).values_list('voltage', flat=True)
                                    .order_by('voltage').distinct(), empty_label=u'Напряжение',
                                     )

    power = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True).values_list('power', flat=True)
                                   .order_by('power').distinct(), empty_label=u'Мощность',
                                   )

    type = forms.ModelChoiceField(queryset=Parameter.objects.filter(
                                    category=CategoryParameter.objects.filter(name=u'Способ пуска',is_active=True),
                                    is_active=True),
                                    empty_label="Способ пуска",
                                )

    atributes = forms.ModelChoiceField(queryset=Atribute.objects.filter(
        category=CategoryAtribute.objects.filter(name=u'Коммуникация', is_active=True), is_active=True),
        label='Атрибуты', required=False, empty_label=u'Коммуникация',
        )

    manufacturer = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True)
                                            .values_list('manufacturer__name', flat=True).distinct(),
                                            required=False, empty_label=u'Производитель',
                                          )
