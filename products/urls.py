from django.urls import path
from products import views

urlpatterns = [
   
   path('<slug>/',views.get_products , name="get_products"),
]
