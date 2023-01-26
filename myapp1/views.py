from django.shortcuts import render
from django.contrib.auth.models import User, Group

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import generics
# from rest_framework.parsers import JSONParser

from .models import MenuItem, Category
from .serializer import MenuItemSerializer, CategorySerizlizer

class MenuItems(generics.ListCreateAPIView):
    # authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def post(self, request):
        print(request.data)
        
        title = request.data['title']
        price = request.data['price']
        featured = request.data['featured']
        category = request.data['category']
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            # x = MenuItem.objects.create(title=title, price=price, featured=featured)
            # x.save()
            x = MenuItem(title=title, price=price, featured=featured, category_id=category)
            x.save()
            return Response({'message': 'Nice'})
        return Response("You're not authenticated")
    def put(self, request):
        id = request.data['id']
        title = request.data['title']
        price = request.data['price']
        featured = request.data['featured']
        category = request.data['category']
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            x = MenuItem.objects.get(pk=id)
            x.title = title
            x.price = price
            x.featured = featured
            x.category_id = category
            x.save()
            return Response({'message': 'Nice update'})
        return Response("You're not authenticated")


class CategoriesView(generics.ListCreateAPIView):
    # authentication_classes = []
    # permission_classes = [IsAuthenticated, IsAdminUser] #disables permission
    queryset = Category.objects.all()
    serializer_class = CategorySerizlizer
    def post(self, request):
        # data = JSONParser.parse(request)
        # print(data)
        print(request.data)
        slug = request.data['slug']
        title = request.data['title']
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            # x = MenuItem.objects.create(title=title, price=price, featured=featured)
            # x.save()
            
            x = Category(slug=slug, title=title)
            x.save()
            return Response({'message': 'Nice'})
        return Response("You're not authenticated")











# Manager stuff 
class Manager(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    managers_group = Group.objects.get(name='Manager')
    
        
    def post(self, request):
        username = request.data['username']
        if username:
            user = User.objects.create(username=username)
            self.managers_group.user_set.add(user)
            return Response({'message': 'ok'})
        return Response({'message': 'error'})
    def delete(self, request):
        username = request.data['username']
        if username:
            user = User.objects.create(username=username)
            self.managers_group.user_set.add(user)
            return Response({'message': 'ok'})
        return Response({'message': 'error'})

class UpdateRoles(APIView):
    # queryset = User.objects.all()
    # serializer_class = CategorySerizlizer
    permission_classes = [IsAuthenticated, IsAdminUser]
    delivery_group = Group.objects.get(name='DeliveryCrew')
    def put(self, request, userId):
        user = User.objects.get(pk=userId)
        # role = request.data['data']
        self.delivery_group.user_set.add(user)
        print('Is the user in delivery crew', self.delivery_group.user_set.filter(id=userId).exists()) # checking if this user is aleady assigned to this group
        return Response({'message': 'The role is updated'})



class Delivery(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    delivery_group = Group.objects.get(name='DeliveryCrew')
    
    def post(self, request):
        username = request.data['username']
        if username:
            user = User.objects.create(username=username)
            self.delivery_group.user_set.add(user)
            return Response({'message': 'ok'})
        return Response({'message': 'error'})
    
    def delete(self, request):
        username = request.data['username']
        if username:
            user = User.objects.create(username=username)
            self.delivery_group.user_set.add(user)
            return Response({'message': 'ok'})
        return Response({'message': 'error'})

