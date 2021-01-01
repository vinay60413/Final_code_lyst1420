from rest_framework import viewsets
from .serializers import MenuItemsSerializers
from .models import MenuItems
from ..discountDetails.models import DiscountDetails
from ..product.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
import os, sys

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, str):
            return str(obj)
        return super().default(obj)

@csrf_exempt
def getMenuItems(request, id):
    if request.method == "GET":
        try:
            returnDict = {}
            product = Product.objects.get(id=id)
            queryset = MenuItems.objects.filter(product=product).values()
            # Discount Info extractor
            discountInfoNameLi = []
            for val in Product.objects.filter(id=id).values():
                if val['discountInfo'] != None:
                    discountInfoNameLi = val['discountInfo'].split(',')
            discountDict = []
            for coupon in discountInfoNameLi:
                for val in DiscountDetails.objects.filter(couponName=coupon).values():
                    discountDict.append(val)
            returnDict['discountInfo'] =  discountDict
            # Discount Info Ends

            # Category data maker
            li = []
            category = []
            categoryInd = []
            for item in queryset:
                li.append(item)
                if item['category'] not in categoryInd:
                    categoryInd.append(item['category'])
                    category.append({'title':item['category'],'active':True})
            returnDict['data'] = li 
            temp = []
            setFlag = 0
            ind = 0
            setInd = 0
            ### Poping recommended category to the top
            for item in  category:
                if 'Recommended' == item['title']:
                    temp = category[0]
                    category[0] = item
                    setFlag = 1
                    setInd = ind
                ind+=1
            if setFlag == 1:
                category[setInd] = temp
            
            returnDict['category'] = category
            ### Category adder ends

            return JsonResponse(returnDict,safe=False)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print('Exception at build_alert \nline:',exc_tb.tb_lineno,'\nException:',exc_obj,'\ntype:', exc_type)
            return JsonResponse({'Err':'ER02X'})
    return JsonResponse({'Err':'GET method required'})

class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItems.objects.all().order_by('id')
    serializer_class = MenuItemsSerializers
