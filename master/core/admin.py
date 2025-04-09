from django.contrib import admin
from core.models import Product, Product_Category, Order_Item, Order_Detail, Discount, Product_Inventory, Payment, Order_Detail, \
ProductReview, Wishlist, Address, ProductImages, Staff, Salary

# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['ID_Product','Name', 'Desc', 'Price', 'discount','inventory','Image']
    
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['product','order_detail','Quantity','Note','Image','Total']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['ID_Product_Category','Name','Desc','Image']

class ProductInventoryAdmin(admin.ModelAdmin):
    
    list_display= ['ID_Product_Inventory','Name','Quantity','Updated']

class DiscountAdmin(admin.ModelAdmin):
    list_display= ['ID_Discount','Name','Desc','Discount_Percent', 'Active']

class PaymentAdmin(admin.ModelAdmin):
    list_display=['ID_Payment','Desc','Date','Method','Money']
    
class OrderDetailAdmin(admin.ModelAdmin):
    list_display= ['ID_Order_Detail','user','Payment','Date','Total_Price','Payment_Status','Delivery_Status']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display=['ID_ProductReview','user','product','Review','Rating','Date']

class WishlistAdmin(admin.ModelAdmin):
    list_display= ['user','product','Date']

class AddressAdmin(admin.ModelAdmin):
    list_display= ['user','Address1','Address2','City','Country','Phone']

class StaffAdmin(admin.ModelAdmin):
    list_display = ['ID_Staff','ID_card','Started','Birthday','Position']

class SalaryAdmin(admin.ModelAdmin):
    list_display=['ID_Salary','staff','Date','Desc','Salary','Bonus']
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Product_Category, CategoryAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Product_Inventory, ProductInventoryAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order_Detail, OrderDetailAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order_Item, OrderItemAdmin)
admin.site.register(Staff,StaffAdmin)
admin.site.register(Salary,SalaryAdmin)



