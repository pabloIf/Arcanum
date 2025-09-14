from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils.text import slugify

from .models import Category, Product


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    query = request.GET.get('q', '').strip()

    products = Product.objects.filter(available=True).exclude(image='')

    category = None
    featured_product = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if query:
        query_slug = slugify(query)
        products = products.filter(slug__icontains=query_slug)

        category = None
        featured_product = None

    if not category and not query:
        featured_product = Product.objects.filter(is_featured=True).first()
        if featured_product:
            products = products.exclude(id=featured_product.id)
    

    sort_option = request.GET.get('sort')
    if sort_option:
        products = apply_sort(products, sort_option)

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

def apply_sort(products, sort_option):
        if sort_option == 'price_asc':
            return products.order_by('price')
        elif sort_option == 'price_desc':
            return products.order_by('-price')
        elif sort_option == 'name_asc':
            return products.order_by('name')
        elif sort_option == 'name_desc':
            return products.order_by('-name')
        return products

