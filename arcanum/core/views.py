from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils.text import slugify

from .models import Category, Product


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    query = request.GET.get('q', '')

    if query:
        query_slug = slugify(query)
        products = Product.objects.filter(available=True, slug__icontains=query_slug).exclude(image='')
        category = None
        featured_product = None
    else:
        products = Product.objects.filter(available=True).exclude(image='')
        category = None
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        featured_product = None
        if not category:
            featured_product = Product.objects.filter(is_featured=True).first()
            if featured_product:
                products = products.exclude(id=featured_product.id)

    return render(request, 'core/product/list.html',
                  {'products' : products,
                   'categories' : categories,
                   'category' : category,
                   'featured_product': featured_product,
                   'query': query,
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]

    return render(request, 'core/product/detail.html',
                  {"product" : product,
                  'related_products' : related_products,
    })

