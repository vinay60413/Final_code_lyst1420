from django.db import models
from api.category.models import Category
from django.core.validators import MaxValueValidator

class DiscountDetails(models.Model):
    couponName = models.CharField(max_length=10)
    discounPercentage = models.DecimalField(
        decimal_places=1, max_digits=3, blank=True, null=True, validators=[MaxValueValidator(100)])
    discountCap = models.DecimalField(
        decimal_places=1, max_digits=5, blank=True, null=True, validators=[MaxValueValidator(10000)])
    discountInfo = models.CharField(max_length=50)
    expiryDate = models.DateTimeField()
    def __str__(self):
        return self.couponName