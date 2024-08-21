from django.urls import path
from account import views
# from products.views import add_to_cart

urlpatterns = [
    path("login/",views.user_login, name="login"),
    path("register/",views.register, name="register"),
    path("activate/<email_token>",views.activate_email, name="activate"),
    path("cart/",views.cart ,name="cart"),
    path("add-to-cart/<uid>/",views.add_to_cart,name="add_to_cart"),
    path('update-quantity/<uid>/',views.update_cart_item_quantity, name='update_cart_item_quantity'),
    path('remove-cart-item/<uid>/', views.remove_cart_item, name='remove_cart_item'),
    path("checkout",views.checkout_view,name="chceckout"),
    path("checkout1",views.checkout_view1,name="chceckout1"),
    path("userprofile",views.userprofile,name="UserProfile"),
    path("payments",views.payments ,name="Payments"),
    path("add address",views.add_address, name="add address"),
    path("orders/",views.order_list,name="orders"),
    path("orderplaced",views.orderplaced,name="orderplaced"),
    path("shop",views.shop,name="shop")
]