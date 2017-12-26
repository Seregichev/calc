from django import forms
from items.models import Item
from parameters.models import Parameter, CategoryParameter, Atribute, CategoryAtribute



class AddPowerForm (forms.Form):

    # обозначаем как форма добавления изделий комутации электродвигателя
    appointment = forms.IntegerField(widget=forms.HiddenInput(), initial='add_power_items')

    comment = forms.CharField(required=True,  widget=forms.TextInput(
                                attrs={'placeholder': u'Назначение', 'class': 'form-control'}),
                              error_messages={'required': 'Пожалуйста укажите назначение'},
                              )

    voltage = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True).values_list('voltage', flat=True)
                                    .order_by('voltage').distinct(),
                                     empty_label=u'Напряжение',
                                     error_messages={'required': 'Пожалуйста выберите напряжение'}
                                     )

    power = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True).values_list('power', flat=True)
                                   .order_by('power').distinct(),
                                   empty_label=u'Мощность',
                                   error_messages={'required': 'Пожалуйста выберите мощность'}
                                   )

    type = forms.ModelChoiceField(queryset=Parameter.objects.filter(
                                    category=CategoryParameter.objects.filter(name=u'Способ пуска',is_active=True),
                                    is_active=True),
                                    empty_label=u"Способ пуска",
                                    error_messages={'required': 'Пожалуйста выберите способ пуска'}
                                )

    choise_reverse = forms.BooleanField(label='Реверс', required=False)

    choise_bypass = forms.BooleanField(label='Bypass', required=False)

    atributes = forms.ModelChoiceField(queryset=Atribute.objects.filter(
        category=CategoryAtribute.objects.filter(name=u'Коммуникация', is_active=True), is_active=True),
        label='Атрибуты', required=False, empty_label=u'Коммуникация',
        )

    manufacturer = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True)
                                            .values_list('manufacturer__name', flat=True).distinct(),
                                            required=False, empty_label=u'Производитель',
                                          )
