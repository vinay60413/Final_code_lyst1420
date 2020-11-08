from rest_framework import serializers

from .models import MenuItems


class MenuItemsSerializers(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=True, required=False)

    class Meta:
        model = MenuItems
        #uncomment category if requeired
        fields = ('id', 'name', 'description', 'price', 'image', 'product','review_stars', 'review_counts')
