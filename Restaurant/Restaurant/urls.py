"""
URL configuration for Restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from RestaurantApp import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    #########################################################################################################
    # startup part
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    #########################################################################################################
    # Home Page
    path('',views.home),
    #########################################################################################################
    #Menu 
    path('api/menu/', views.MenuItemListCreate.as_view(), name='menu_list_create'),
    path('menu/',views.menu_view, name='menu'),
    path('menu/<int:pk>/delete/', views.delete_menu_item, name='delete_menu_item'),
    path('menu/<int:pk>/update/', views.update_menu_item, name='update_menu_item'),
    #########################################################################################################
    #Orders
    path('api/orders/', views.OrderListCreate.as_view(), name='orders_list_create'),
    path('orders/', views.order_history_view, name='orders'),
    path('add_item/', views.add_menu_item_view, name='add_menu_item'),
    path('clear_order_history/', views.clear_order_history, name='clear_order_history'),
    #########################################################################################################
    #Cart
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('remove_order/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('print_order_history/', views.print_order_history, name='print_order_history'),
    #########################################################################################################
    #Authentication
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    #End Of Urls
    #########################################################################################################
]


