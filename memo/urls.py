from django.urls import path
from . import views

urlpatterns = [
    path('', views.memo_list, name='home'),
    path('add_item/', views.add_item, name='add_item'),
    path('complete/<int:item_id>/', views.complete, name='complete'),
    path('incomplete/<int:item_id>/', views.incomplete, name='incomplete'),
    path('delete/<int:item_id>/', views.delete, name='delete'),
    path('up/<int:item_id>/', views.up, name='up'),
    path('down/<int:item_id>/', views.down, name='down'),
]
