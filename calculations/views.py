from django.shortcuts import render
from .forms import AddPowerForm
from .models import ItemInEstimate

def adding_power_in_estimate(request):
    session_key = request.session.session_key
    print(session_key)

    form = AddPowerForm(request.POST or None )

    if request.POST:
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print('Yes')
            data = request.POST
            voltage = data["voltage"]
            power = data["power"]

            print("Напряжение %s, Ток %s") % voltage, power
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