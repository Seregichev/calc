from django.shortcuts import render
from .forms import AddPowerForm
from .models import ItemInEstimate
from items.models import Item, ItemCategory
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
        parameter = data["parameter"]

        # В базе данных парметров определяем привязанные категории изделий к параметру опрделенному по типу
        categories_item_in_parameter = Parameter.objects.filter(id=parameter,is_active=True).values(
            'itemcategoryparameter__item_category','itemcategoryparameter__nmb')

        print('Напряжение '+voltage+'В, Мощность '+power+'кВт'+power+'кВт, Тип пуска '+parameter)

        # По привязанным категориям к параметру в цикле добвляем изделий с колличеством заданным в привязанном параметре
        for category_item_in_parameter in categories_item_in_parameter:
            print(str(category_item_in_parameter))
            add_item = Item.objects.filter(category=category_item_in_parameter.get('itemcategoryparameter__item_category'),
                                           is_active=True, power=power, voltage=voltage).first()
            nmb = category_item_in_parameter.get('itemcategoryparameter__nmb')
            created = ItemInEstimate.objects.create(session_key=session_key, item_id=add_item.id, is_active=True,
                                                    calculate=None,
                                                    nmb=nmb, comment=comment)
            if not created:
                print('Not created ',comment, voltage, power, parameter)


        # if type == '1':
        #     # Добавить цикл для обхода всех вложенных категорий изделий и оставить только одну функцию добавления
        #     add_power_item(session_key=session_key, comment=comment, category="Автоматический выключатель",
        #                    voltage=voltage, power=power, type=type)
        #     add_power_item(session_key=session_key, comment=comment, category="Контактор",
        #                    voltage=voltage, power=power, type=type)
            # раскоментировать когда в базе появяться тепловые реле
            # add_power_item(session_key=session_key, comment=comment, category="Тепловое реле",
            #                voltage=voltage, power=power, type=type)


            # if not created:
            #     print("not created")
            #     new_product.nmb += int(nmb)
            #     new_product.save(force_update=True)




            # user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})
            # order = Order.objects.create(user=user, costumer_name=name, costumer_phone=phone, status_id=1)
            #
            # print(data.items)
            # for name, value in data.items():
            #     if name.startswith('product_in_basket_'):
            #         product_in_basket_id = name.split('product_in_basket_')[1]
            #         product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
            #         print(product_in_basket_id)
            #         product_in_basket.nmb = value
            #         product_in_basket.order = order
            #         product_in_basket.save(force_update=True)
            #
            #         ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
            #                                       price_per_item=product_in_basket.price_per_item,
            #                                       total_price=product_in_basket.total_price,
            #                                       order=order)
            #         return HttpResponseRedirect(request.META['HTTP_REFERER'])
            #     else:
            #         print ('No')

    return render(request, 'items/estimate.html', locals())