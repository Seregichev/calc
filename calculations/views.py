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
        return render_to_response('estimate/estimate.html', {'error': msg_error})

    else:
        return created

def delete_comment_in_estimate(session_key, comment):
    delete_items = ItemInEstimate.objects.filter(session_key=session_key, comment=comment)
    delete_items.delete()

def base_calculate(request):
    session_key = request.session.session_key

    # выдаем таблицу для отображения изделий в смете
    items_in_estimate = ItemInEstimate.objects.filter(session_key=session_key, is_active=True, calculate__isnull=True)

    # отображаем форму запроса для формирования силовой
    form = AddPowerForm(request.POST or None)

    if request.POST:
        data = request.POST

        #пытаемся получить коментарий для удаления
        try:
            delete_comment = data["delete_comment"]
        except:
            delete_comment=None

        # если коментарий удаления есть, то удалем из сметы
        if delete_comment:
            delete_comment_in_estimate(session_key=session_key, comment=delete_comment )
        # иначе добавляем изделия в смету
        else:
            # Выгружаем данные из посылки
            comment = data["comment"]
            voltage = data["voltage"]
            power = data["power"]
            type = data["type"]
            atributes = data["atributes"] or None
            manufacturer = data["manufacturer"] or None

            # по типу пуска в БД параметров забираем связанные активные модели, а именно - категорию и колличество изделий
            categories_item_in_parameter = Parameter.objects.filter(id=type,is_active=True).values(
                'itemcategoryparameter__item_category', 'itemcategoryparameter__nmb',
                'itemcategoryparameter__item_paramater_do_more')

            # обходим циклом все связанные изделий из подобранных
            for category_item_in_parameter in categories_item_in_parameter:

                add_item = Item.objects.filter(
                    category=category_item_in_parameter.get('itemcategoryparameter__item_category'), is_active=True)

                # если в параметре для соответсвующей категории указан подбор на ступень выше, то...
                if category_item_in_parameter.get('itemcategoryparameter__item_paramater_do_more'):
                    # получаем устройство соответсвующее параметрам отдбора с условием подбора мощности на ступень выше
                    add_item = add_item.filter(power__gt=power, voltage__gte=voltage)
                else:
                    # иначе получаем устройство соответсвующее параметрам отдбора или выше по мощности и напряжению
                    add_item = add_item.filter(power__gte=power, voltage__gte=voltage)

                if manufacturer:
                    add_item = add_item.filter(manufacturer__name=manufacturer).first()
                else:
                    add_item = add_item.first()

                # получаем количество изделий
                nmb = category_item_in_parameter.get('itemcategoryparameter__nmb')

                print(add_item)

                # если устройство найдено то...
                if add_item:

                    # добавляем устройство в смету
                    created_item = created_item_in_estimate(session_key=session_key, item_id=add_item.id, is_active=True,
                                                            calculate=None, nmb=nmb, comment=comment)
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
                else:
                    delete_comment_in_estimate(session_key=session_key, comment=comment)
                    msg_error = u'В базе данных нет элементов с таким критериями. Пожалуйста измените запрос'


            # Проверка добавленных в корзину изделий на наличие в них запрошенного атрибута, если нет то удаляем и выводим сообщение об ошибке
            if not ItemInEstimate.objects.filter(session_key=session_key, is_active=True,  comment=comment, item__atributes=atributes):
                delete_comment_in_estimate(session_key=session_key, comment=comment)
                msg_error = u'В базе данных нет элементов с таким атрибутом. Пожалуйста измените запрос'

    # Разрешаем модифицировать Post запрос
    if not request.POST._mutable:
        request.POST._mutable = True
    # Стираем значение коментария добавления
    request.POST["comment"]=''
    request.POST["delete_comment"]=None

    return render(request, 'calculate/base_calculate.html', locals())