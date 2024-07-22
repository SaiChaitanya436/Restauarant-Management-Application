from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import MenuItem, Order, Cart, CartItem
from .serializers import MenuItemSerializer, OrderSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib.auth.models import Group
from .forms import MenuItemForm, SignUpForm
from django.http import HttpResponse
import csv


#create your views here

#########################################################################################################
# Class-Based Views
class MenuItemListCreate(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticated,IsAdminUser) #Only authenticated users have access 

class OrderListCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,IsAdminUser) #Only authenticated users have access 

#User Login Part
class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'RestaurantApp/login.html', {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        return render(request, 'RestaurantApp/login.html', {'form': form})

#User Logout Part
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
#########################################################################################################

#########################################################################################################
# Method-Based Views
@login_required
def home(request):
    return render(request,"RestaurantApp/base.html")
#########################################################################################################

@login_required
def menu_view(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'RestaurantApp/menu.html', {'menu_items': menu_items})
#########################################################################################################

@login_required
def order_history_view(request):
    orders = Order.objects.filter(customer = request.user)
    orders_data = []
    
    for order in orders:
        orders_data.append({
            'id': order.id,
            'customer_name': order.customer.username,  # Assuming customer is a User instance
            'order_date': order.order_date.strftime('%d/%m/%y'),  # Format date as DD/MM/YY
            'total_amount': order.total_amount,
            # Add more fields as needed
        })
    
    return render(request, 'RestaurantApp/order_history.html', {'orders': orders_data})
#########################################################################################################

@login_required
def clear_order_history(request):
    Order.objects.all().delete()
    return redirect('orders')
#########################################################################################################

@login_required
def print_order_history(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_history.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer Name','Order Date', 'Total Amount'])

    orders = Order.objects.all()
    for order in orders:
        writer.writerow([order.id,order.customer.username, order.order_date, order.total_amount])
    return response

#########################################################################################################
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            # Assign user to selected group
            group_name = form.cleaned_data.get('group')
            if group_name:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            return redirect('login')
    else:
        form = SignUpForm()
    
    groups = Group.objects.all()
    return render(request, 'RestaurantApp/signup.html', {'form': form, 'groups': groups})

#########################################################################################################
@login_required
def add_menu_item_view(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')  # Redirect to the menu page after successful form submission
    else:
        form = MenuItemForm()
    return render(request, 'RestaurantApp/add_item.html', {'form': form})

#########################################################################################################
@login_required
def delete_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('menu')
    return render(request, 'RestaurantApp/delete_menu_item.html', {'item': item})

#########################################################################################################
@login_required
def update_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    form = MenuItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('menu')
    return render(request, 'RestaurantApp/update_menu_item.html', {'form': form})

#########################################################################################################
@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=item)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    
    # Update cart total amount
    cart.total_amount = sum(item.total_price for item in cart.cart_items.all())
    cart.save()
    
    return redirect('menu')

#########################################################################################################
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, cart__user=request.user, menu_item__id=item_id)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    cart = cart_item.cart
    cart.total_amount = sum(item.total_price for item in cart.cart_items.all())
    cart.save()
    
    return redirect('cart_view')

#########################################################################################################
@login_required
def confirm_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    Order.objects.create(customer=request.user, total_amount=cart.total_amount)
    
    for cart_item in cart.cart_items.all():
        cart_item.menu_item.quantity_sold += cart_item.quantity
        cart_item.menu_item.save()
    
    cart.cart_items.all().delete()
    cart.total_amount = 0
    cart.save()
    
    return redirect('orders')

#########################################################################################################
@login_required
def cart_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'RestaurantApp/cart.html', {'cart': cart})

#########################################################################################################
