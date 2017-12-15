from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from items.models import *

# def item (request):
#     items = Item.objects.filter(is_active=True)
#     categories = ItemCategory.objects.filter(is_active=True)
#     powers_items = Item.objects.filter(is_active=True).values('power').order_by().distinct()
#
#     return render(request, 'items/item.html', locals())
#
# def home (request):
#     return render(request, 'items/home.html', locals())
#
# def filter_category_items(request):
#     return_dict = dict()
#     print('Запрос пришел!')
#     print(request.POST)
#     data = request.POST
#     filter_category_items = data.get("filter_category_id")
#     filter_power = data.get("filter_power", None)
#
#     if filter_power:
#         items = Item.objects.filter(category=filter_category_items, power=filter_power, is_active=True)
#     else:
#         items = Item.objects.filter(category=filter_category_items, is_active=True)
#
#     return_dict["filtered_item"] = list()
#     for item in items:
#         item_dict = dict()
#         item_dict['name'] = item.name
#         item_dict['power'] = item.power
#
#         return_dict['filtered_item'].append(item_dict)
#
#     return JsonResponse(return_dict)