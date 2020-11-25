from rest_framework import viewsets
from .serializers import MenuItemsSerializers
from .models import MenuItems
from ..product.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, str):
            return str(obj)
        return super().default(obj)

@csrf_exempt
def getMenuItems(request, id):
    if request.method == "GET":
        product = Product.objects.get(id=id)
        queryset = MenuItems.objects.filter(product=product).values()
        returnDict = {}
        li = []
        category = []
        for item in queryset:
            li.append(item)
            if item['category'] not in category:
                category.append({'title':item['category'],'active':True})
        returnDict['data'] = li 
        returnDict['category'] = category
        return JsonResponse(returnDict,safe=False)
    return JsonResponse({'Err':'GET method required'})

class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItems.objects.all().order_by('id')
    serializer_class = MenuItemsSerializers
