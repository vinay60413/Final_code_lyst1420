from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=True, required=False)

    class Meta:
        model = Product
        #uncomment category if requeired
        fields = ('id', 'name', 'description', 'price', 'image', 'category','review_stars', 'review_counts')
