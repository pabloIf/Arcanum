from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=164, db_index=True)
    slug = models.SlugField(max_length=164, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("core:product_list_by_category", kwargs={"category_slug": self.slug})
    
    
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=164, db_index=True)
    slug = models.SlugField(max_length=164, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("core:product_detail", kwargs={"id": self.id, "slug": self.slug})
    