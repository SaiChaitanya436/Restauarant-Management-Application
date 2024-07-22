from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.conf import settings

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name 

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_items = models.ManyToManyField(MenuItem)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.customer.username}'

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.menu_item.price * self.quantity

@receiver(post_save,sender = settings.AUTH_USER_MODEL)
def createAuthToken(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user=instance)