from django.shortcuts import render, render_to_response
from .forms import AddPowerForm
from .models import ItemInEstimate
from items.models import Item
from parameters.models import Parameter

# функция добавления изделия в смету или выдачи ошибки
def created_item_in_estimate(session_key, item_id, is_active, calculate, nmb, comment):
    try:
        created = ItemInEstimate.objects.create(session_key=session_key, item_id=item_id, is_active=is_active,
                                        calculate=calculate, nmb=nmb, comment=comment)
    except:
        msg_error = u'Невозможно добавить изделие в смету. Обратитесь в тех.поддержку'
        render_to_response('items/estimate.html', {'error': msg_error})

    else:
        return created


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
                created_item = created_item_in_estimate(session_key=session_key, item_id=add_item.id, is_active=True,
                                                        calculate=None, nmb=nmb, comment=comment)

                global last_required
                global last_required_nmb
                last_required = None
                last_required_nmb = None

                # циклом обходим дополнительные изделия связанные с добавленным в смету изделием
                for adding_item in Item.objects.filter(id=created_item.item_id).values(
                        'main_item__adding_item',
                        'main_item__required',
                        'main_item__nmb',
                        'main_item__adding_item__atributes')\
                        .order_by('main_item__required','main_item__adding_item__atributes').reverse():

                    # Если доп. изделие обязательное для этого изделия
                    if adding_item.get('main_item__required'):
                        # И если атрибут из формы равен атрибуту обязательного изделия
                        if str(adding_item.get('main_item__adding_item__atributes')) == str(atributes):
                            created_item_in_estimate(session_key=session_key,
                                                    item_id=adding_item.get('main_item__adding_item'),
                                                    is_active=True,
                                                    calculate=None,
                                                    nmb=adding_item.get('main_item__nmb'),
                                                    comment=comment
                                                    )

                            last_required = None
                            last_required_nmb = None
                            break
                        # иначе записываем последнее обязательное изделие
                        else:
                            last_required = adding_item.get('main_item__adding_item')
                            last_required_nmb = adding_item.get('main_item__nmb')

                    else:
                        # если обязательные изделия были, но больше не будут из-за сортировки в цикле то добавляем его
                        if last_required:
                            created_item_in_estimate(session_key=session_key,
                                                     item_id=last_required,
                                                     is_active=True,
                                                     calculate=None,
                                                     nmb=last_required_nmb,
                                                     comment=comment
                                                     )
                            last_required = None
                            last_required_nmb = None
                            break
                        # если у дополнительного изделия совпали атрибуты с формой атрибута, то добавляем
                        if str(adding_item.get('main_item__adding_item__atributes')) == str(atributes):

                            created_item_in_estimate(session_key=session_key,
                                                    item_id=adding_item.get('main_item__adding_item'),
                                                    is_active=True,
                                                    calculate=None,
                                                    nmb=adding_item.get('main_item__nmb'),
                                                    comment=comment
                                                    )
                            last_required = None
                            last_required_nmb = None
                            break




        # Сюда нужно добавить проверку корзины по наличию хотябы одного устройства с атрибутом фильтрации,
        # если такового нет, то удаляем весь подбор с данным коментарием
        print(u'Кот проходит')

    return render(request, 'items/estimate.html', locals())