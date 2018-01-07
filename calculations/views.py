from django.shortcuts import render
from .forms import AddPowerForm, AddControlForm
from .models import ItemInEstimate
from items.models import Item
from parameters.models import Parameter
from uuid import uuid4
from django.db.models import Sum, F


# функция добавления изделия в смету или выдачи ошибки
def created_item_in_estimate(session_key, uuid_id, item_id, is_active, calculate, nmb, comment):
    created = ItemInEstimate.objects.create(session_key=session_key, uuid_id=uuid_id, item_id=item_id,
                                            is_active=is_active, calculate=calculate, nmb=nmb, comment=comment)
    if created:
        return created
    else:
        global msg_error
        msg_error = u'Невозможно добавить изделие в смету. Обратитесь в тех.поддержку'
        return locals()
# функция удаления из сметы всех изделий по совпадению сессии и коментария
def delete_uuid_id_in_estimate(session_key, uuid_id):
    delete_items = ItemInEstimate.objects.filter(session_key=session_key, uuid_id=uuid_id)
    delete_items.delete()

# функция добавления изделий коммутации привода в смету
def add_power_items_in_estimate(session_key, data):
    # глобальная переменная для вывода ошибки
    global msg_error

    # переменная служащая для понимания, все ли изделия добавили или что-то не нашли. True значит не нашли что-то.
    not_found_item = False

    # создаем уникальный идентификатор
    uuid_id = uuid4()

    # Выгружаем данные из посылки
    comment = u'Привод '+data["comment"]
    voltage = data["voltage"]
    power = data["power"]
    type = data["type"]
    atributes = data.get('atributes') or None
    manufacturer = data.get('manufacturer') or None
    manufacturer_terminals = data.get('manufacturer_terminals') or None
    choise_reverse = data.get('choise_reverse', False)
    choise_bypass = data.get('choise_bypass', False)

    # по типу пуска в БД параметров забираем связанные активные модели, а именно - категорию и колличество изделий
    categories_item_in_parameter = Parameter.objects.filter(id=type, is_active=True).values(
        'itemcategoryparameter__item_category',
        'itemcategoryparameter__nmb',
        'itemcategoryparameter__do_more',
        'itemcategoryparameter__revers',
        'itemcategoryparameter__bypass',
    )
    # получаем категорию клемм из параметра категории клемм
    category_terminal_in_parameter = Parameter.objects.filter(name__startswith='Категория клемм',
                                                              is_active=True).values(
                                                                'itemcategoryparameter__item_category').first()

    # обходим циклом все связанные изделий из подобранных
    for category_item_in_parameter in categories_item_in_parameter:

        add_item = Item.objects.filter(category=category_item_in_parameter.get('itemcategoryparameter__item_category'),
                                       is_active=True)

        # если в параметре для соответсвующей категории указан подбор на ступень выше, то...
        if category_item_in_parameter.get('itemcategoryparameter__do_more'):
            # получаем устройство соответсвующее параметрам отдбора с условием подбора мощности на ступень выше
            add_item = add_item.filter(power__gt=power, voltage__gte=voltage)
        else:
            # иначе получаем устройство соответсвующее параметрам отдбора или выше по мощности и напряжению
            add_item = add_item.filter(power__gte=power, voltage__gte=voltage)
        # если категория в обходе цикла есть категория клемм присвоенных в параметре
        if category_terminal_in_parameter['itemcategoryparameter__item_category'] \
                == category_item_in_parameter['itemcategoryparameter__item_category']:
            # если в request есть производитель клемм то
            if manufacturer_terminals:
                # фильтруем с учетом производителя
                add_item = add_item.filter(manufacturer__name=manufacturer_terminals)
        # если категория в обходе цикла не равно категории клемм присвоенного в параметре
        else:
            # если в запросе присутствует производитель фильтруем изделия из категории по производителю
            if manufacturer:
                # фильтруем с учетом производителя
                add_item = add_item.filter(manufacturer__name=manufacturer)
        # иначе выбираем первый подходящий
        add_item = add_item.first()

        # получаем количество изделий
        nmb = category_item_in_parameter.get('itemcategoryparameter__nmb')

        # если нужен реверс то увеличиваем
        if choise_reverse and category_item_in_parameter.get('itemcategoryparameter__revers'):
            nmb += nmb
        # если нужен bypass то увеличиваем
        if choise_bypass and category_item_in_parameter.get('itemcategoryparameter__revers'):
            nmb += nmb

        # если устройство найдено то...
        if add_item:

            # добавляем устройство в смету
            created_item = created_item_in_estimate(session_key=session_key,
                                                    uuid_id=uuid_id,
                                                    item_id=add_item.id,
                                                    is_active=True,
                                                    calculate=None,
                                                    nmb=nmb,
                                                    comment=comment)
            # определяем глобальные переменные
            global last_required
            global last_required_nmb
            last_required = None
            last_required_nmb = None

            # циклом обходим дополнительные изделия связанные с добавленным в смету изделием
            for adding_item in Item.objects.filter(id=created_item.item_id).values(
                    'main_item__adding_item',
                    'main_item__required',
                    'main_item__nmb',
                    'main_item__adding_item__atributes') \
                    .order_by('main_item__required', 'main_item__adding_item__atributes').reverse():

                # Если доп. изделие обязательное для этого изделия
                if adding_item.get('main_item__required'):
                    # И если атрибут из формы равен атрибуту обязательного изделия
                    if atributes and str(adding_item.get('main_item__adding_item__atributes')) == str(atributes):
                        created_item_in_estimate(session_key=session_key,
                                                 uuid_id=uuid_id,
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
                                                 uuid_id=uuid_id,
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
                    if atributes and str(adding_item.get('main_item__adding_item__atributes')) == str(atributes):
                        created_item_in_estimate(session_key=session_key,
                                                 uuid_id=uuid_id,
                                                 item_id=adding_item.get('main_item__adding_item'),
                                                 is_active=True,
                                                 calculate=None,
                                                 nmb=adding_item.get('main_item__nmb'),
                                                 comment=comment
                                                 )
                        last_required = None
                        last_required_nmb = None
                        break
            # если цикл for по указанным в параметре категориям изделия закончился а мы не добавили последнее обязательное изделие то добавляем его
            if last_required:
                created_item_in_estimate(session_key=session_key,
                                         uuid_id=uuid_id,
                                         item_id=last_required,
                                         is_active=True,
                                         calculate=None,
                                         nmb=last_required_nmb,
                                         comment=comment
                                         )
                last_required = None
                last_required_nmb = None

        else:
            not_found_item=True
            msg_error += u'В базе данных нет элементов с критериями %s %s кВт, %s В. ' % (manufacturer, power, voltage)

    # Проверка добавленных в корзину изделий на наличие в них запрошенного атрибута, если нет то удаляем и выводим сообщение об ошибке
    if not ItemInEstimate.objects.filter(session_key=session_key, is_active=True, comment=comment, item__atributes=atributes):
        not_found_item = True
        msg_error += u'В базе данных нет элементов с атрибутом %s. ' % (str(atributes))

    if not_found_item:
        delete_uuid_id_in_estimate(session_key=session_key, uuid_id=uuid_id)
        msg_error += u'Пожалуйста измените запрос.'
    return locals()

# функция добавления изделий управления в смету
def add_control_items_in_estimate(session_key, data):
    # глобальная переменная для вывода ошибки
    global msg_error

    # переменная служащая для понимания, все ли изделия добавили или что-то не нашли. True значит не нашли что-то.
    not_found_item = False

    # создаем уникальный идентификатор
    uuid_id = uuid4()

    # Выгружаем данные из посылки
    comment = u'Управление '+data["comment"]
    type = data["type"]
    atributes = data.get('atributes') or None
    manufacturer = data.get('manufacturer') or None
    series = data.get('series') or None

    discret_inputs = data.get('discret_inputs') or 0
    first_discret_inputs = discret_inputs
    discret_outputs = data.get('discret_outputs') or 0
    first_discret_outputs = discret_outputs
    analog_inputs = data.get('analog_inputs') or 0
    first_analog_inputs = analog_inputs
    analog_outputs = data.get('analog_outputs') or 0
    first_analog_outputs = analog_outputs
    temperature_inputs = data.get('temperature_inputs') or 0
    first_temperature_inputs = temperature_inputs

    manufacturer_terminals = data.get('manufacturer_terminals') or None
    manufacturer_relays = data.get('manufacturer_relays') or None

    # по типу пуска в БД параметров забираем связанные активные модели, а именно - категорию и колличество изделий
    categories_item_in_parameter = Parameter.objects.filter(id=type, is_active=True).values(
        'itemcategoryparameter__item_category',
        'itemcategoryparameter__nmb',
        'itemcategoryparameter__amount_fixed',
        'itemcategoryparameter__main_category',
        'itemcategoryparameter__common_category',
        'value'
    )
    # получаем категорию клемм из параметра категории клемм
    category_terminal_in_parameter = Parameter.objects.filter(name__startswith='Категория клемм',
                                                              is_active=True).values(
                                                                'itemcategoryparameter__item_category').first()
    # получаем категорию промежуточных реле из параметра категории промежуточных реле
    category_relay_in_parameter = Parameter.objects.filter(name__startswith='Категория промежуточных реле',
                                                              is_active=True).values(
                                                                'itemcategoryparameter__item_category').first()

    # получаем напряжение из парметра выбранного типа упарвления -> величина
    voltage = Parameter.objects.get(id=type, is_active=True).value

    # обходим циклом все связанные изделий из подобранных
    for category_item_in_parameter in categories_item_in_parameter:

        add_item = Item.objects.filter(
            category=category_item_in_parameter.get('itemcategoryparameter__item_category'),
            is_active=True)

        # получаем колличество изделий из категории издилий в параметре
        nmb = category_item_in_parameter.get('itemcategoryparameter__nmb')

        # если основная категория изделий в параметре
        if category_item_in_parameter.get('itemcategoryparameter__main_category'):
            # фильтруем выдачу изделий по производителю , серии и напряжению
            add_item = add_item.filter(manufacturer__name=manufacturer, series=series, voltage__gte=voltage)

        # если общая категория изделий в параметре
        elif category_item_in_parameter.get('itemcategoryparameter__common_category'):

            # если категория изделий равна категории клемм из параметра "категория клемм"
            if category_terminal_in_parameter['itemcategoryparameter__item_category'] \
                    == category_item_in_parameter['itemcategoryparameter__item_category']:
                # если в request есть производитель клемм то
                if manufacturer_terminals:
                    # фильтруем с учетом производителя
                    add_item = add_item.filter(manufacturer__name=manufacturer_terminals, voltage__gte=voltage)
                # колличество равно сумме запрашиваемых выводов
                nmb = int(nmb) * (int(first_discret_inputs) + int(first_discret_outputs) + int(first_analog_inputs)
                                  + int(first_analog_outputs) + int(first_temperature_inputs))

            # иначе если категория изделий равна категории реле из параметра "категория промежуточных реле"
            elif category_relay_in_parameter['itemcategoryparameter__item_category'] \
                    == category_item_in_parameter['itemcategoryparameter__item_category']:
                # если в request есть производитель реле то
                if manufacturer_relays:
                    # фильтруем с учетом производителя
                    add_item = add_item.filter(manufacturer__name=manufacturer_relays, voltage__gte=voltage)
                # колличество равно сумме запрашиваемых дискретных выводов
                nmb = int(nmb) * (int(first_discret_inputs) + int(first_discret_outputs))

            # во всех остальных случаях
            else:
                # фильтруем выдачу изделий по напряжению
                add_item = add_item.filter(voltage__gte=voltage)
                # колличество равно сумме запрашиваемых выводов
                nmb = int(nmb) * (int(first_discret_inputs) + int(first_discret_outputs) + int(first_analog_inputs)
                                  + int(first_analog_outputs) + int(first_temperature_inputs))

        # в остальных случаях
        else:
            # фильтруем выдачу изделий по напряжению
            add_item = add_item.filter(manufacturer__name=manufacturer, series=series, voltage__gte=voltage)
            # сортируем выдачу в порядке возрастания
            add_item = add_item.order_by('-discret_input','-discret_output','-analog_input','-analog_output',
                                         '-temperature_input',)
            # если нашлись изделия
            if add_item:
                # если первое изделие из выборки содержит данный тип вывода то определяем кол-во выводов по потребности от запроса
                if add_item[0].discret_input:
                    nmb = round(int(discret_inputs)/int(add_item[0].discret_input) + .5)
                elif add_item[0].discret_output:
                    nmb = round(int(discret_outputs)/int(add_item[0].discret_output) + .5)
                elif add_item[0].analog_input:
                    nmb = round(int(analog_inputs)/int(add_item[0].analog_input) + .5)
                elif add_item[0].analog_output:
                    nmb = round(int(analog_outputs)/int(add_item[0].analog_output) + .5)
                elif add_item[0].temperature_input:
                    nmb = round(int(temperature_inputs)/int(add_item[0].temperature_input) + .5)

        # если изделие из выборки есть и для него указано колличество
        if add_item and nmb > 0:
            # добавляем изделие в смету
            created_item = created_item_in_estimate(session_key=session_key,
                                                    uuid_id=uuid_id,
                                                    item_id=add_item[0].id,
                                                    is_active=True,
                                                    calculate=None,
                                                    nmb=nmb,
                                                    comment=comment)
            if not category_item_in_parameter.get('itemcategoryparameter__common_category'):
                # находим добавляемое устройство
                item = Item.objects.get(id=add_item[0].id)
                # уменьшаем колличество необходимых выводов на кол-во добавленных выводов с изделием, добавленным в смету
                discret_inputs = int(discret_inputs) - (int(item.discret_input) * nmb)
                discret_outputs = int(discret_outputs) - (int(item.discret_output) * nmb)
                analog_inputs = int(analog_inputs) - (int(item.analog_input) * nmb)
                analog_outputs = int(analog_outputs) - (int(item.analog_output) * nmb)
                temperature_inputs = int(temperature_inputs) - (int(item.temperature_input) * nmb)

            # определяем глобальные переменные
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
                    .order_by('main_item__required', 'main_item__adding_item__atributes').reverse():

                # Если доп. изделие обязательное для этого изделия
                if adding_item.get('main_item__required'):
                    # И если атрибут из формы равен атрибуту обязательного изделия
                    if atributes and str(adding_item.get('main_item__adding_item__atributes')) == str(atributes):
                        created_item_in_estimate(session_key=session_key,
                                                 uuid_id=uuid_id,
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
                                                 uuid_id=uuid_id,
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
                    if atributes and str(adding_item.get('main_item__adding_item__atributes')) == str(atributes):
                        created_item_in_estimate(session_key=session_key,
                                                 uuid_id=uuid_id,
                                                 item_id=adding_item.get('main_item__adding_item'),
                                                 is_active=True,
                                                 calculate=None,
                                                 nmb=adding_item.get('main_item__nmb'),
                                                 comment=comment
                                                 )
                        last_required = None
                        last_required_nmb = None
                        break
            # если цикл for по указанным в параметре категориям изделия закончился а мы не добавили последнее обязательное изделие то добавляем его
            if last_required:
                created_item_in_estimate(session_key=session_key,
                                         uuid_id=uuid_id,
                                         item_id=last_required,
                                         is_active=True,
                                         calculate=None,
                                         nmb=last_required_nmb,
                                         comment=comment
                                         )
                last_required = None
                last_required_nmb = None

    # Получаем общее колличество добавленных в смету выводов
    check_items = ItemInEstimate.objects.filter(session_key=session_key, is_active=True, uuid_id=uuid_id)\
        .exclude(item__category__itemcategoryparameter__common_category=True)
    check_items_discret_inputs = check_items.aggregate(total_discret_inputs=Sum(F('item__discret_input')*F('nmb')))
    check_items_discret_inputs = check_items_discret_inputs.get('total_discret_inputs')

    check_items_discret_outputs = check_items.aggregate(total_discret_output=Sum(F('item__discret_output') * F('nmb')))
    check_items_discret_outputs = check_items_discret_outputs.get('total_discret_output')

    check_items_analog_inputs = check_items.aggregate(total_analog_inputs=Sum(F('item__analog_input') * F('nmb')))
    check_items_analog_inputs = check_items_analog_inputs.get('total_analog_inputs')

    check_items_analog_outputs = check_items.aggregate(total_analog_outputs=Sum(F('item__analog_output') * F('nmb')))
    check_items_analog_outputs = check_items_analog_outputs.get('total_analog_outputs')

    check_items_temperature_inputs = check_items.aggregate(total_temperature_inputs=Sum(F('item__temperature_input') * F('nmb')))
    check_items_temperature_inputs = check_items_temperature_inputs.get('total_temperature_inputs')

    # Проверяем не добавили ли мы каких либо запрашиваемых выводов
    if int(first_discret_inputs) > int(check_items_discret_inputs) \
            or int(first_discret_outputs) > int(check_items_discret_outputs)\
            or int(first_analog_inputs) > int(check_items_analog_inputs) \
            or int(first_analog_outputs) > int(check_items_analog_outputs)\
            or int(first_temperature_inputs) > int(check_items_temperature_inputs):
        # Если не смогли добавить то выводим сообщение об ошибке и удаляем
        not_found_item = True
        msg_error += u'Не возможно подобрать при таких условиях.' \
                     u'Задано DI = %s, а подобрано %s. ' \
                     u'Задано DQ = %s, а подобрано %s. ' \
                     u'Задано AI = %s, а подобрано %s. ' \
                     u'Задано AQ = %s, а подобрано %s. ' \
                     u'Задано TI = %s, а подобрано %s. ' \
                     % (str(first_discret_inputs), str(check_items_discret_inputs),
                        str(first_discret_outputs), str(check_items_discret_outputs),
                        str(first_analog_inputs), str(check_items_analog_inputs),
                        str(first_analog_outputs), str(check_items_analog_outputs),
                        str(first_temperature_inputs), str(check_items_temperature_inputs))
    # если найден флаг ненайденных изделий, то
    if not_found_item:
        # удаляем из сметы по uuid
        delete_uuid_id_in_estimate(session_key=session_key, uuid_id=uuid_id)
        msg_error += u'Пожалуйста измените запрос.'

    return locals()

# функция удаления изделий из сметы
def delete_items(session_key, data):

    # получаем uuid из request
    uuid_id = data["uuid_id"]

    # по uuid удаляем из сметы все совпавщие изделия
    delete_uuid_id_in_estimate(session_key=session_key, uuid_id=uuid_id)

    return locals()

def base_calculate(request):
    # определение глобальной переменной для вывода ошибки
    global msg_error
    msg_error = ''
    global aria_expanded
    aria_expanded = ''

    session_key = request.session.session_key

    # выдаем таблицу для отображения изделий в смете
    items_in_estimate = ItemInEstimate.objects.filter(session_key=session_key, is_active=True, calculate__isnull=True)

    # отображаем форму запроса для формирования силовой
    power_form = AddPowerForm(request.POST or None)

    # отображаем форму запроса для формирования управляющей
    control_form = AddControlForm(request.POST or None)


    if request.POST:
        data = request.POST
        print(data)

        print(data["appointment"])

        if data["appointment"] == 'add_power_items':
            add_power_items_in_estimate(session_key=session_key, data=data)

        if data["appointment"] == 'add_control_items':
            add_control_items_in_estimate(session_key=session_key, data=data)

        if data["appointment"] == 'delete_items':
            delete_items(session_key=session_key, data=data)

        aria_expanded = data["appointment"]

    # Разрешаем модифицировать Post запрос
    if not request.POST._mutable:
        request.POST._mutable = True
    # Стираем значение коментария добавления
    request.POST["comment"] = ''

    return render(request, 'calculate/base_calculate.html', {'items_in_estimate': items_in_estimate,
                                                             'power_form': power_form,
                                                             'control_form': control_form,
                                                             'msg_error': msg_error,
                                                             'aria_expanded': aria_expanded,
                                                             })