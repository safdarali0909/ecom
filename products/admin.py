from django.contrib import admin
from products.models import *


admin.site.register(category)
admin.site.register(coupon)


class ProductImageAdmin(admin.StackedInline):
    model = productsImage

class ProductAdmin(admin.ModelAdmin):
    list_display =['product_name','price']
    inlines = [ProductImageAdmin]
@admin.register(colorvariant)
class colorvarient(admin.ModelAdmin):
    list_display=['color_name','price']
    model=colorvariant
@admin.register(sizevariant)
class sizevariant(admin.ModelAdmin):
    list_display=['size_name','price']
    model=sizevariant

admin.site.register(product,ProductAdmin)
admin.site.register(productsImage)