from rest_framework import serializers
from .models import MenuItem, Category, Order, Cart


        
        
class CategorySerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
        
class MenuItemSerializer(serializers.ModelSerializer):
    # category = CategorySerizlizer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(method_name='calculate_price')
    # unit_price = serializers.DecimalField(source='unit_price', max_digits=6, decimal_places=2)
    # quantity = serializers.IntegerField(source= 'quantity')
    class Meta:
        model = Cart
        fields = ['id', 'quantity', 'unit_price', 'price', 'menuitem_id', 'user_id']
    def calculate_price(self, cart: Cart):
        print(cart.unit_price * cart.quantity)
        return cart.unit_price * cart.quantity