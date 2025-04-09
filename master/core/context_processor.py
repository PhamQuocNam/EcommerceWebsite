from core.models import Product, Product_Category, Order_Item, Order_Detail, Discount, Product_Inventory, Payment, Order_Detail, \
ProductReview, Wishlist, Address, ProductImages, Staff, Salary

def default(request):
    categories = Product_Category.objects.all()
    try:
        address= Address.objects.get(user= request.user)
    except:
        address=None
    
    
    return {
        'categories': categories,
        'address':address
        }    