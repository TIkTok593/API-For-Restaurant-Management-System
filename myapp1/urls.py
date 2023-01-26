from django.urls import path

from rest_framework.authtoken.views import ObtainAuthToken

from . import views

urlpatterns = [
    path('menu-items/', views.MenuItems.as_view()),
    path('category/', views.CategoriesView.as_view()),
    path('obtain-auth-token', ObtainAuthToken.as_view()),
    path('users/<int:userId>/groups', views.UpdateRoles.as_view()),
    path('users/<int:userId>/cart/menu-items', views.CartViews.as_view()),
    path('orders/', views.OrderView.as_view()),
    # path('orders/<int:orderId>', views.OrderView2.as_view()),
]