from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from products.models import product
# from accounts.models import cart,cartItems
from products.models import *
# Create your views here.
from django.utils import timezone
from account.models import Order
from django.shortcuts import get_object_or_404

def get_products(request, slug):
    # Fetch the product based on the slug
    product_obj = get_object_or_404(product, slug=slug)
    context = {'product': product_obj}

    # Handle size and price update if specified
    if request.GET.get('size'):
        size = request.GET.get('size')
        price = product_obj.get_product_price_by_size(size)
        context['selected_size'] = size
        context['updated_price'] = price

    # Get the delivery date
    delivery_date = timezone.now().date() + timedelta(days=7)
    context['delivery_date'] = delivery_date
    
    return render(request, 'products/product.html', context)




# def add_to_cart(request, uid):
#     variant = request.GET.get('variant')
#     product_obj = product.objects.get(uid=uid)
#     user = request.user
#     cart_obj, _ = cart.objects.get_or_create(user=user, is_paid=False)
#     cart_item_obj, _ = cartItems.objects.get_or_create(cart=cart_obj, product=product_obj)

#     if variant:
#         size_variant = sizevariant.objects.get(size_name=variant)
#         cart_item_obj.size_variant = size_variant
#     else:
#         cart_item_obj.size_variant = None

#     cart_item_obj.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

      

      
     


