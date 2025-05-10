from core.models import Product, Product_Category, Order_Item, Order_Detail, Discount, Product_Inventory, Payment, Order_Detail, \
ProductReview, Wishlist, ProductImages, Staff, Salary

def default(request):
    categories = Product_Category.objects.all()
    
    
    return {
        'categories': categories
        }    