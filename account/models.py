from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from products.models import *
from base.emails import send_account_activation_email 
from django.utils import timezone
from datetime import timedelta

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to="static/profile", null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    organization = models.CharField(max_length=100, blank=True, null=True)
    work_phone = models.CharField(max_length=20, blank=True, null=True)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def get_cart_counter(self):
        return CartItems.objects.filter(cart__is_paid=False,cart__user=self.user).count()

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="carts")
    is_paid =models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.email
class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name="cart_items")
    product = models.ForeignKey(product, on_delete=models.SET_NULL,blank=True,null=True)
    color_variant =models.ForeignKey(colorvariant,on_delete=models.SET_NULL,blank=True,null=True)
    size_variant =models.ForeignKey(sizevariant,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.PositiveIntegerField(default=1)

    def get_product_price(self):
        price=[self.product.price]

        if self.color_variant:
            color_variant_price = self.color_variant.price
            price.append(color_variant_price)
         

        if self.size_variant:
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
         
        return sum(price)
    def get_total_price(self):
        return self.quantity * self.get_product_price()
    
    def __str__(self):
        return self.cart.user.email
    

class chceckout(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255,default="not provided")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20,default="not provided")

    def __str__(self):
        return f'{self.full_name}, {self.city}, {self.state}, {self.zip_code}'


class PaymentMethod(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit or Debit Card'),
        ('net_banking', 'Net Banking'),
        ('upi', 'UPI'),
        ('emi', 'EMI'),
        ('cod', 'Cash on Delivery'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES,default="Cash on Delivery")
    details = models.CharField(max_length=255, blank=True, null=True)  # To store additional details like UPI ID or bank name

    def __str__(self):
        return f'{self.get_method_display()} for {self.user.username}'



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Order Placed')
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True, blank=True) 
    total_price = models.IntegerField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)  # New field

    def save(self, *args, **kwargs):
        if not self.delivery_date:
            self.delivery_date = timezone.now().date() + timedelta(days=7)  # Example: 7 days from order date
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'


@receiver(post_save, sender=User)
def send_emial_token(sender,instance,created,**kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email,email_token,)

    except Exception as e:
        print(e)
