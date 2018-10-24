from django.urls import path
from . import views

urlpatterns = [
    path('', views.show),
    path('order_list', views.show_orderset),
    path('order_list.json', views.get_orderset),
]
