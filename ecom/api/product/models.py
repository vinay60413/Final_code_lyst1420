from django.db import models
from api.category.models import Category
from django.core.validators import MaxValueValidator
# Create your models here.

# Restaurant or store details
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    discountInfo = models.CharField(max_length=50, blank=True, null=True)
    stock = models.CharField(max_length=50)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    review_stars = models.DecimalField(
        decimal_places=1, max_digits=2, blank=True, null=True, validators=[MaxValueValidator(5)])
    review_counts = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
