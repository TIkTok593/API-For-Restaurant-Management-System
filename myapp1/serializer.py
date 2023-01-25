from rest_framework import serializers
from .models import MenuItem, Category


        
        
class CategorySerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
        
class MenuItemSerializer(serializers.ModelSerializer):
    # category = CategorySerizlizer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']