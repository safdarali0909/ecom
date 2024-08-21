from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from account.models import Cart,CartItems,Profile,DeliveryAddress,PaymentMethod,Order
from products.models import *
from django.shortcuts import get_object_or_404
import logging
from django.utils.timezone import localtime
from django.utils import timezone
import pytz

logger = logging.getLogger(__name__)

# Create your views here.
def user_login(request):
     if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, "Account Not Found!")
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
             messages.warning(request, 'your account is not verified!')
             return HttpResponseRedirect(request.path_info)
        
        
        if 'email_verified' in request.GET:
          messages.success(request, 'Your email has been verified. You can now log in.')
        
        user_obj = authenticate(username= email,password=password)
        if user_obj:
            login(request, user_obj)
            # messages.success(request, 'Logged in successfully!')
            return redirect('/')
        
        if 'email_verified' in request.GET:
            messages.success(request, 'Your email has been verified. You can now log in.')

             
        messages.warning(request, 'invalid credentials')
        return HttpResponseRedirect(request.path_info)
            


        
     return render(request, 'accounts/login.html')
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('frist')
        last_name = request.POST.get('last')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        user_obj = User.objects.filter(username=email)

        if user_obj.exists():
            messages.warning(request, "Email is already Exist Please Try Another Email ")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(first_name=first_name, last_name=last_name,username=email,email=email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'an email has been sent successfully to your mail')
        return HttpResponseRedirect(request.path_info)

            


    return render(request, 'accounts/register.html')

def activate_email(request,email_token):
   try:
        
        user= Profile.objects.get(email_token = email_token)
        user.is_email_verified=True
        user.save()
        messages.success(request, 'Your Email Has Been Verified You Can Login Now')
        return redirect('login')
   except Exception as e:
        return HttpResponse("invalid token")
        
def add_to_cart(request, uid):
    variant = request.GET.get('variant')
    product_obj = product.objects.get(uid=uid)
    user = request.user
    cart_obj, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item_obj, _ = CartItems.objects.get_or_create(cart=cart_obj, product=product_obj)

    if variant:
        size_variant = sizevariant.objects.get(size_name=variant)
        cart_item_obj.size_variant = size_variant
    else:
        cart_item_obj.size_variant = None

    cart_item_obj.save()
    print(f"Added to cart: {cart_item_obj}") 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   
def cart(request):
    cart_obj = Cart.objects.filter(is_paid=False, user=request.user).first()
    cart_items = CartItems.objects.filter(cart=cart_obj)
    cart_total = sum(item.get_total_price() for item in cart_items)
    flat_rate_shipping = 40 
    cart_total_plus_shipping = cart_total + flat_rate_shipping
    

    context = {
        'cartItems': cart_items,
        'cart': cart_obj,
        'cart_total': cart_total,
        'flat_rate_shipping': flat_rate_shipping,
        'cart_total_plus_shipping': cart_total_plus_shipping,
    }
    return render(request, 'accounts/cart.html', context=context)
    


def update_cart_item_quantity(request, uid):
    if request.method == 'POST':
        item = get_object_or_404(CartItems,  uid=uid,cart__user=request.user, cart__is_paid=False)
        new_quantity = int(request.POST.get('quantity',0))
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
            messages.success(request, 'Quantity updated successfully.')
        else:
            messages.error(request, 'Invalid quantity.')
    return redirect('cart')

def remove_cart_item(request,uid):
    item = get_object_or_404(CartItems, uid=uid, cart__user=request.user, cart__is_paid=False)
    item.delete()
    messages.success(request, 'Item removed from cart')
    return redirect('cart')
    


def checkout_view(request):
    cart_obj = Cart.objects.filter(is_paid=False, user=request.user).first()
    cart_items = CartItems.objects.filter(cart=cart_obj)

    if request.method == 'POST':
        # Handle address data submission if necessary
        address_data = {
            'Full_name': request.POST.get('full_name'),
            'Street': request.POST.get('street'),
            'City': request.POST.get('city'),
            'State': request.POST.get('state'),
            'Zip_code': request.POST.get('zip_code')
        }

        delivery_address, created = DeliveryAddress.objects.update_or_create(
            user=request.user,
            defaults=address_data
        )

        # Handle payment method
        payment_method = request.POST.get('payment_method')
        upi_id = request.POST.get('upi_id')
        bank = request.POST.get('bank')  # For net banking if needed

        PaymentMethod.objects.update_or_create(
            user=request.user,
            defaults={
                'method': payment_method,
                'details': upi_id if payment_method == 'upi' else bank
            }
        )

        # Check if 'place_order' button was clicked
        if 'place_order' in request.POST:
            # Loop through all items in the cart and create an order for each
            for item in cart_items:
                Order.objects.create(
                    user=request.user,
                    product=item.product,  # Link the product to the order
                    quantity=item.quantity,  # Quantity of the product in the cart
                    order_date=timezone.now(),
                    status='Order Placed',
                    delivery_address=delivery_address,
                    total_price=item.get_total_price()
                )
            print(Order.delivery_address)
            # Mark the cart as paid
            cart_obj.is_paid = True
            cart_obj.save()

            # Redirect to order confirmation
            return redirect('orderplaced')  # Make sure to define this URL

    # Fetch data to display on the checkout page
    delivery_address = DeliveryAddress.objects.filter(user=request.user).first()
    payment_methods = PaymentMethod.objects.filter(user=request.user)
    products = product.objects.all()  # Ensure the correct model name `Product`

    context = {
        'delivery_address': delivery_address,
        'payment_methods': payment_methods,
        'products': products,
        'cartItems': cart_items,
        'cart': cart_obj,
    }

    return render(request, 'accounts/checkout.html', context)





def userprofile(request):
   profile = Profile.objects.get(user=request.user)
    
   if request.method == 'POST':
        # Update profile fields
        profile.name = request.POST.get('name', profile.name)
        profile.title = request.POST.get('title', profile.title)
        profile.organization = request.POST.get('organization', profile.organization)
        profile.work_phone = request.POST.get('work_phone', profile.work_phone)
        profile.mobile_phone = request.POST.get('mobile_phone', profile.mobile_phone)
        profile.email = request.POST.get('email', profile.email)
        
        # Handle file upload
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
        
        profile.save()
        return redirect('/')
    
   return render(request, 'accounts/userprofile.html', {'profile': profile})

def payments(request):
    return render(request,'accounts/payment.html')
def add_address(request):
    return render(request,'accounts/add_address.html')
def order_list(request):
    ist = pytz.timezone('Asia/Kolkata')
    orders = Order.objects.filter(user=request.user)
    for order in orders:
        order.order_date_ist = localtime(order.order_date, ist)
    return render(request, 'accounts/orders.html', {'orders': orders})
def orderplaced(request):
    return render(request, 'base/orderplaced.html')
def shop(request):
    # Get all category names
    categories = category.objects.values_list('category_name', flat=True).distinct()

    # Get selected category from query parameters
    category_name = request.GET.get('category')

    # If a category is selected, filter products by that category; otherwise, get all products
    if category_name:
        products = product.objects.filter(category__category_name=category_name)
    else:
        products = product.objects.all()

    # Pass both products and categories to the context
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_name,
    }

    return render(request, 'accounts/shop.html', context)

def checkout_view1(request):
    cart_obj = Cart.objects.filter(is_paid=False, user=request.user).first()
    cart_items = CartItems.objects.filter(cart=cart_obj)
    

    context = {
        'cartItems': cart_items,
        'cart': cart_obj,
    }
    return render(request, 'accounts/checkout1.html',context=context)