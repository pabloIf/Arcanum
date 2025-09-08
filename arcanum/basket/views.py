from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.models import Product
from .basket import Basket

@require_POST
def basket_add(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    basket.add(product=product, quantity=1)
    return redirect(f"{request.META.get('HTTP_REFERER', '/')}?cart_open=1")

@require_POST
def basket_remove(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    basket.remove(product=product)
    return redirect(f"{request.META.get('HTTP_REFERER', '/')}?cart_open=1")