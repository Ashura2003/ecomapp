from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    '''
    This is the serializer class for the Item model which is used to convert model instances into JSON format and vice versa.
    '''
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'stock' ]
        read_only_fields = ['id']

    def create(self, validated_data):
        '''
        Create a new item instance with the provided validated data.
        '''
        return Item.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        '''
        Update an existing item instance with the provided validated data.
        '''
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()
        return instance
    
    