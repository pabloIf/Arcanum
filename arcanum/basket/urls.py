from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    # path('', views.basket_deatail, name='basket_detail'),
    path('add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('decrement/<int:product_id>', views.basket_decrement, name='basket_decrement'),
    path('remove/<int:product_id>/', views.basket_remove, name='basket_remove')
]
