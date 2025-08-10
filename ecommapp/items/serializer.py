from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    '''
    This is the serializer class for the Item model which is used to convert model instances into JSON format and vice versa.
    '''
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'stock' ]


    def create(self, validated_data):
        '''
        Create a new item instance with the provided validated data.
        '''
        return Item.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        '''
        Update an existing item instance with the provided validated data.
        '''
        updatable_fields = ['name','description', 'price', 'rating', 'stock']
        for field in updatable_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance:
            raise serializers.ValidationError("Item not found.")
        return representation

    def validate_items(self, value):
        if Item.objects.filter(name=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Item Already Exist.")
        return value
