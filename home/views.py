from django.shortcuts import render
from products.models import product


def index(request):
    context={'products':product.objects.all()}
    return render(request, 'home/index.html',context)

def About(request):
    return render(request, 'home/about.html')