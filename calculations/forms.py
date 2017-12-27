from django import forms
from items.models import Item
from parameters.models import Parameter, CategoryParameter, Atribute, CategoryAtribute



class AddPowerForm (forms.Form):

    category_terminals = Parameter.objects.filter(name__startswith='Категория клемм', is_active=True).values(
        'itemcategoryparameter__item_category').first()
    category_terminals = category_terminals.get('itemcategoryparameter__item_category')

    # обозначаем в параметре inital как форма добавления изделий комутации электродвигателя
    appointment = forms.IntegerField(widget=forms.HiddenInput(), initial='add_power_items')

    comment = forms.CharField(required=True,  widget=forms.TextInput(
                                attrs={'placeholder': u'Назначение', 'class': 'form-control'}),
                              error_messages={'required': 'Пожалуйста укажите назначение'},
                              )

    voltage = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True).values_list('voltage', flat=True)\
                                    .order_by('voltage').distinct(),
                                     empty_label=u'Напряжение',
                                     error_messages={'required': 'Пожалуйста выберите напряжение'}
                                     )

    power = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True).values_list('power', flat=True)\
                                   .order_by('power').distinct(),
                                   empty_label=u'Мощность',
                                   error_messages={'required': 'Пожалуйста выберите мощность'}
                                   )

    type = forms.ModelChoiceField(queryset=Parameter.objects.filter(
                                    category=CategoryParameter.objects.filter(name=u'Способ пуска',is_active=True),
                                    is_active=True),
                                    error_messages={'required': 'Пожалуйста выберите способ пуска'}
                                )

    choise_reverse = forms.BooleanField(label='Функция Реверс',
                                        help_text=u'Добавляет в схему дополнительные изделия для запуска двигателя в обратную сторону',
                                        required=False)

    choise_bypass = forms.BooleanField(label='Функция Bypass',
                                       help_text=u'Добавляет в схему дополнительные изделия для реализации Bypass',
                                       required=False)

    atributes = forms.ModelChoiceField(queryset=Atribute.objects.filter(
        category=CategoryAtribute.objects.filter(name=u'Коммуникация', is_active=True), is_active=True),
        label='Атрибуты', required=False,
        )

    manufacturer = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True)\
                                            .exclude(category=int(category_terminals))\
                                            .values_list('manufacturer__name', flat=True).distinct(),
                                            required=False,
                                          )

    manufacturer_terminals = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True,
                                            category=int(category_terminals))\
                                            .values_list('manufacturer__name', flat=True).distinct(),
                                            required=False,
                                          )
