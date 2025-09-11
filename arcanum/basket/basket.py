from django.conf import settings
from core.models import Product
from decimal import Decimal

class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.CART_SESSION_ID)
        if not basket:
            basket = self.session[settings.CART_SESSION_ID] = {}
        self.basket = basket


    def add(self, product, quantity=1):
        product_id = str(product.id)

        if product_id not in self.basket:
            self.basket[product_id] = {
                'name': product.name,
                'quantity': 0,
                'price': str(product.price)
            }
        
        self.basket[product_id]['quantity'] += quantity
        self.save()

    def decrement(self, product):
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['quantity'] -= 1
            if self.basket[product_id]['quantity'] < 1:
                del self.basket[product_id]
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)

        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            if 'product' not in item:
                continue
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.basket.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())
    
    def clean(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()