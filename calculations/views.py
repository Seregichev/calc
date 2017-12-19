from django.shortcuts import render, render_to_response
from .forms import AddPowerForm
from .models import ItemInEstimate
from items.models import Item
from parameters.models import Parameter


def adding_power_in_estimate(request):
    session_key = request.session.session_key
    print(session_key)
    items_in_estimate = ItemInEstimate.objects.filter(session_key=session_key, is_active=True, calculate__isnull=True)

    form = AddPowerForm(request.POST or None)

    if request.POST:
        print(request.POST)
        # Выгружаем данные из посылки
        data = request.POST
        voltage = data["voltage"]
        power = data["power"]
        comment = data["comment"]
        type = data["type"]
        atributes = data["atributes"]

        print(atributes)
        print('Напряжение ' + voltage + 'В, Мощность ' + power + 'кВт, Тип пуска ' + type)

        # по типу пуска в БД параметров забираем связанные активные модели, а именно - категорию и колличество изделий
        categories_item_in_parameter = Parameter.objects.filter(id=type,is_active=True).values(
            'itemcategoryparameter__item_category', 'itemcategoryparameter__nmb',
            'itemcategoryparameter__item_paramater_do_more')

        # обходим циклом все связанные изделий из подобранных
        for category_item_in_parameter in categories_item_in_parameter:
            print(str(category_item_in_parameter))

            # если в параметре для соответсвующей категории указан подбор на ступень выше, то...
            if category_item_in_parameter.get('itemcategoryparameter__item_paramater_do_more'):
                # получаем устройство соответсвующее параметрам отдбора с условием подбора мощности на ступень выше
                add_item = Item.objects.filter(
                    category=category_item_in_parameter.get('itemcategoryparameter__item_category'),
                    is_active=True, power__gt=power, voltage__gte=voltage).first()
            else:
                # иначе получаем устройство соответсвующее параметрам отдбора или выше по мощности и напряжению
                add_item = Item.objects.filter(
                    category=category_item_in_parameter.get('itemcategoryparameter__item_category'),
                    is_active=True, power__gte=power, voltage__gte=voltage).first()
            # получаем количество изделий
            nmb = category_item_in_parameter.get('itemcategoryparameter__nmb')

            # если устройство найдено то...
            if add_item:
                # добавляем устройство в смету
                created = ItemInEstimate.objects.create(session_key=session_key, item_id=add_item.id, is_active=True,
                                                        calculate=None, nmb=nmb, comment=comment)
                # если нет то выводим сообщение об ошибке
                if not created:
                    print('Not created')
                    msg_error = u'Невозможно добавить изделие в смету. Обратитесь в тех.поддержку'
                    render_to_response('items/estimate.html', {'error': error})
            # если устройство не найдено то...
            else:
                # выводим сообщение об ошибке
                print('Not found')
                error = u'Невозможно подобрать изделие по заданным критериям подбора.'
                render_to_response('items/estimate.html', {'error': error})

        # Сюда нужно добавить проверку корзины по наличию хотябы одного устройства с атрибутом фильтрации,
        # если такового нет, то удаляем весь подбор с данным коментарием
        print(u'Кот проходит')

    return render(request, 'items/estimate.html', locals())