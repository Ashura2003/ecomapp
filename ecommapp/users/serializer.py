from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import CartItem, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name' , 'last_name', 'email', 'username',  'date_joined', 'is_active', 'is_staff', 'user_type']
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

    

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for token authentication.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user'] = UserSerializer(user).data
        return data

    class Meta:
        model = Token
        fields = ['key', 'user'] 

class CustomCartItemSerializer(serializers.ModelSerializer):
    '''
    Serializer for CartItem model to handle cart items in the e-commerce application.
    '''
    class Meta:
        model = CartItem
        fields = ['id', 'user', 'item', 'quantity']
        read_only_fields = ['id', 'user']
    
    def create(self, validated_data):
        '''
        Create a new cart item instance with the provided validated data.
        '''
        user = validated_data.get('user')
        item = validated_data.get('item')
        
        # Check if the item already exists in the user's cart
        cart_item, created = CartItem.objects.get_or_create(user=user, item=item)
        
        if not created:
            # If it exists, update the quantity
            cart_item.quantity += validated_data.get('quantity', 1)
        else:
            # If it doesn't exist, set the quantity
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
    
    def validate_quantity(self, value):
        '''
        Validate that the quantity is a positive integer.
        '''
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value
    
    