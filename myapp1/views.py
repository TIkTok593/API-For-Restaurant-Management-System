from django.shortcuts import render
from django.contrib.auth.models import User, Group
import requests
import datetime
from requests.auth import HTTPBasicAuth

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import generics
# from rest_framework.parsers import JSONParser

from .models import MenuItem, Category, Order, Cart
from .serializer import MenuItemSerializer, CategorySerizlizer, OrderSerializer, CartSerializer
from .CustomerAuthentication import ExampleAuthentication

class MenuItems(generics.ListCreateAPIView):
    # authentication_classes = [] #disables authentication
    permission_classes = [IsAuthenticated] #disables permission

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
            x = Category(slug=slug, title=title)
            x.save()
            return Response({'message': 'Nice'})
        return Response("You're not authenticated")
    def put(self, request):
            id = request.data['id']
            title = request.data['title']
            slug = request.data['slug']
            if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
                x = Category.objects.get(pk=id)
                x.title = title
                x.slug = slug
                x.save()
                return Response({'message': 'Nice update'})
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



# class OrderView1(generics.ListCreateAPIView)



class CartViews(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [ExampleAuthentication]
    # queryset = Cart.objects.all()
    # serializer_class = CartSerializer
    def get(self, request, userId):
        if not (request.user.groups.filter(name='DeliveryCrew').exists()  or request.user.groups.filter(name='Manager').exists()):
            lst = []
            for cart_item in Cart.objects.all():
                print(cart_item.user_id)
                if cart_item.user_id == userId:
                    lst.append(({'id': cart_item.id}, {'menu_item_id': cart_item.menuitem_id}, {'cart_item_id': cart_item.quantity}, {'cart_item_price': cart_item.unit_price}))
            return Response(lst)
        return Response({'message': 'You are not customer'})
    def post(self, request, userId):
        if not (request.user.groups.filter(name='DeliveryCrew').exists()  or request.user.groups.filter(name='Manager').exists()):
            id = request.data['id']
            quantity = request.data['quantity']
            unit_price= request.data['unit_price']
            # print(quantity, unit_price)
            # print(type(quantity), type(unit_price))
            price = float(int(quantity) * float(unit_price))
            # print(price)
            menu_item = request.data['menu_item']
            # user_id = request.data['user_id']
            x = Cart(id, quantity=quantity, unit_price=unit_price, price=price, menuitem_id= menu_item, user_id=userId)
            x.save()
            payload = {'request_type': request.POST, 'cart': x, 'user': request.user}
            # basic = HTTPBasicAuth('user', 'pass')
            requests.post('http://127.0.0.1:8000/api/orders/', params=payload)
            return Response({'message': 'Everything is updated'})
        return Response({'message': 'You are not customer'})
        
    def delete(self, request, userId):
        if not (request.user.groups.filter(name='DeliveryCrew').exists()  or request.user.groups.filter(name='Manager').exists()):
            x = Cart.objects.get(pk=request.data['id'], user_id=userId)
            print(x)
            x.delete()
            return Response({'message': 'Ok, deletion is done'})
        return Response({'message': 'You are not customer'})

class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    id = 0
    def post(self, request):
        # if not (request['user'].groups.filter(name='DeliveryCrew').exists()  or request.user.groups.filter(name='Manager').exists()):
        print('hehheheheh')
        delivery_group = Group.objects.filter(name='DeliveryCrew')
        print(f'delivery_group= {delivery_group}')
            # x = Order(self.id, False, request['cart'].price, datetime.date, delivery_group.user_set)
            # self.id += 1