from django import forms
from items.models import Item
from parameters.models import Parameter, CategoryParameter, Atribute, CategoryAtribute

categories_terminals = Parameter.objects.filter(name__startswith='Категория клемм', is_active=True).values(
        'itemcategoryparameter__item_category')
category_terminals = categories_terminals.first().get('itemcategoryparameter__item_category')

categories_relays = Parameter.objects.filter(name__startswith='Категория промежуточных реле', is_active=True).values(
        'itemcategoryparameter__item_category')
category_relays = categories_relays.first().get('itemcategoryparameter__item_category')

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
                                     error_messages={'required': 'Пожалуйста выберите напряжение'},
                                     widget=forms.Select(attrs={'class': 'form-control'})
                                     )

    power = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True).values_list('power', flat=True)\
                                   .order_by('power').distinct(),
                                   empty_label=u'Мощность',
                                   error_messages={'required': 'Пожалуйста выберите мощность'},
                                   widget=forms.Select(attrs={'class': 'form-control'})
                                   )

    type = forms.ModelChoiceField(queryset=Parameter.objects.filter(
                                    category=CategoryParameter.objects.filter(name=u'Способ пуска',is_active=True),
                                    is_active=True),
                                    error_messages={'required': 'Пожалуйста выберите способ пуска'},
                                    widget = forms.Select(attrs={'class': 'form-control'}),
                                    )

    choise_reverse = forms.BooleanField(label='Функция Реверс',
                                        help_text=u'Добавляет в схему дополнительные изделия для запуска двигателя в обратную сторону',
                                        required=False)

    choise_bypass = forms.BooleanField(label='Функция Bypass',
                                       help_text=u'Добавляет в схему дополнительные изделия для реализации Bypass',
                                       required=False
                                       )

    atributes = forms.ModelChoiceField(queryset=Atribute.objects.filter(
        category=CategoryAtribute.objects.filter(name=u'Коммуникация', is_active=True), is_active=True),
        label='Атрибуты', required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
        )

    manufacturer = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True)\
                                            .exclude(category=int(category_terminals))\
                                            .values_list('manufacturer__name', flat=True).distinct(),
                                            required=False,
                                            widget=forms.Select(attrs={'class': 'form-control'})
                                            )

    manufacturer_terminals = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True,
                                            category=int(category_terminals))\
                                            .values_list('manufacturer__name', flat=True).distinct(),
                                            required=False,
                                            widget=forms.Select(attrs={'class': 'form-control'})
                                            )

class AddControlForm(forms.Form):

    # обозначаем в параметре inital как форма добавления изделий комутации электродвигателя
    appointment = forms.IntegerField(widget=forms.HiddenInput(), initial='add_control_items')

    comment = forms.CharField(required=True, widget=forms.TextInput(
                                attrs={'placeholder': u'Назначение', 'class': 'form-control'}),
                                error_messages={'required': 'Пожалуйста укажите назначение'},
                                )

    type = forms.ModelChoiceField(queryset=Parameter.objects.filter(
                                    category=CategoryParameter.objects.filter(name=u'Тип управления', is_active=True),
                                    is_active=True),
                                    error_messages={'required': 'Пожалуйста выберите тип управления'},
                                    widget=forms.Select(attrs={'class': 'form-control'})
    )

    manufacturer = forms.ModelChoiceField(queryset=Parameter.objects.filter(
        category=CategoryParameter.objects.filter(name=u'Тип управления', is_active=True))\
                                          .values_list('itemcategoryparameter__item_category__item__manufacturer__name',
                                           flat=True).distinct(), widget=forms.Select(attrs={'class': 'form-control'})
                                          )

    series = forms.ModelChoiceField(queryset=Parameter.objects.filter(
        category=CategoryParameter.objects.filter(name=u'Тип управления', is_active=True)) \
                                          .values_list('itemcategoryparameter__item_category__item__series',
                                                       flat=True).distinct(),
                                          widget=forms.Select(attrs={'class': 'form-control'})
                                          )

    discret_inputs = forms.IntegerField(required=True,
                                        error_messages={'required': 'Пожалуйста выберите кол-во дискретных входов'},
                                        widget=forms.NumberInput(attrs={'class': 'form-control'})
                                        )

    discret_outputs = forms.IntegerField(required=True,
                                       error_messages={'required': 'Пожалуйста выберите кол-во дискретных выходов'},
                                       widget=forms.NumberInput(attrs={'class': 'form-control'})
                                       )

    analog_inputs = forms.IntegerField(required=False,
                                       error_messages={'required': 'Пожалуйста выберите кол-во аналоговых входов'},
                                       widget=forms.NumberInput(attrs={'class': 'form-control'})
                                       )

    analog_outputs = forms.IntegerField(required=False,
                                        error_messages={'required': 'Пожалуйста выберите кол-во аналоговых выходов'},
                                        widget=forms.NumberInput(attrs={'class': 'form-control'})
                                        )

    temperature_inputs = forms.IntegerField(required=False,
                                       error_messages={'required': 'Пожалуйста выберите кол-во температурных входов'},
                                       widget=forms.NumberInput(attrs={'class': 'form-control'})
                                       )

    atributes = forms.ModelChoiceField(queryset=Parameter.objects.filter(
        category=CategoryParameter.objects.filter(name=u'Тип управления', is_active=True))\
                                       .values_list('itemcategoryparameter__item_category__item__atributes__name',
                                                    flat=True).distinct(),
                                       required=False,
                                       widget=forms.Select(attrs={'class': 'form-control'})
                                       )

    manufacturer_relays = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True,
                                                    category=int(category_relays))\
                                                    .values_list('manufacturer__name', flat=True).distinct(),
                                                    required=False,
                                                    widget=forms.Select(attrs={'class': 'form-control'})
                                                    )

    manufacturer_terminals = forms.ModelChoiceField(queryset=Item.objects.filter(is_active=True,
                                            category=int(category_terminals))\
                                            .values_list('manufacturer__name', flat=True).distinct(),
                                            required=False,
                                            widget=forms.Select(attrs={'class': 'form-control'})
                                            )


