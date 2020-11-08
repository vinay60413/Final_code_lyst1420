from rest_framework import routers
from django.urls import path, include

from . import views

router = routers.DefaultRouter()
router.register(r'', views.MenuItemsViewSet)

urlpatterns = [
    path('<str:id>/', views.getMenuItems, name='Menu.getMenuItems'),
]