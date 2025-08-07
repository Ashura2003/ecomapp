from items.models import Item
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import CartItem, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name' , 'last_name', 'email', 'password', 'username',  'date_joined', 'is_active', 'is_staff', 'user_type']
        read_only_fields = ['id', 'date_joined', 'is_active', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        '''
        Create a new user instance with the provided validated data.
        '''
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)

        if user.user_type == 'seller':
            user.is_staff = True
        
        user.save()
        return user
    
    
    def update(self, instance, validated_data):
        '''
        Update an existing user instance with the provided validated data.
        '''
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Username already exists.")
        return value



class CustomCartItemSerializer(serializers.ModelSerializer):
    '''
    Serializer for CartItem model to handle cart items in the e-commerce application.
    '''
    user = serializers.SlugRelatedField(
        read_only = True,
        slug_field = 'username'
    )

    item = serializers.SlugRelatedField(
        queryset = Item.objects.all(),
        slug_field = 'name'
    )

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'item', 'quantity']
        read_only_fields = ['id', 'user']
    
    def create(self, validated_data):
        '''
        Create a new cart item instance with the provided validated data.
        '''
        request = self.context.get('request')
        user = request.user  # ✅ Get the logged-in user from context

        item = validated_data.get('item')

        cart_item, created = CartItem.objects.get_or_create(user=user, item=item)

        if not created:
            cart_item.quantity += validated_data.get('quantity', 1)
        else:
            cart_item.quantity = validated_data.get('quantity', 1)

        cart_item.save()
        return cart_item

    
    def update(self, instance, validated_data):
        '''
        Update an existing cart item instance with the provided validated data.
        '''
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance
    
    def get_user_cart(self):
        '''
        Retrieve all cart items for the given user.
        '''
        request = self.context.get('request')
        user = request.user

        cart = CartItem.objects.all().filter(user = user)

        return cart
    
    def validate_quantity(self, value):
        '''
        Validate that the quantity is a positive integer.
        '''
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value
    
    