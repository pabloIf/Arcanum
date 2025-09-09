from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'is_featured', 'created']
    list_filter = ['category', 'available', 'is_featured', 'created']
    list_editable = ['available', 'is_featured', 'price']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ['name']