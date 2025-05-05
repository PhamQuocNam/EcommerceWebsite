from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


STATUS_CHOICE = [
        ('process', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

STATUS=[
    ("draft","Draft"),
    ("disabled","Disabled"),
    ("rejected","Rejected"),
    ("in_review","In Review"),
    ("published","Published")
]

PAYMENT_CHOICE = [
        ('Pay_on_Delivery', 'Pay On Delivery'),
        ('Paypal', 'Paypal'),
        ('Bank_Transfer', 'Bank Transfer')
    ]

RATING = [
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★" )
]

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.Name, filename)

################################### Product Management ################################


class Discount(models.Model):
    """
    Represents a discount campaign that can be applied to products to reduce their price.
    Includes discount percentage, name, description, and optional image.
    """
    
    ID_Discount= ShortUUIDField(unique=True, length=10, max_length=20, prefix="DISCOUNT", alphabet='abcdefgh12345')
    Name = models.CharField(max_length=100)
    Desc= models.TextField(null=True, blank=True, default ='This is the discount')
    Discount_Percent = models.DecimalField(max_digits=10, decimal_places=2, default="0.1")
    Active = models.BooleanField(default=False)
    Image = models.ImageField(upload_to='campaign-image', null=True)
    class Meta:
        verbose_name_plural= "Discounts"
    
    def __str__(self):
        return self.Desc
    
    def get_discount(self):
        return int(self.Discount_Percent*100)
    
    def is_active(self):
        return self.Active
    
    def get_desc(self):
        return self.Desc
    
    def get_name(self):
        return self.Name 
    
    

    
class Product_Inventory(models.Model):
    """
    Tracks inventory details for products, including quantity, unit of measure, and last update time.
    Used to manage stock availability.
    """
    
    ID_Product_Inventory= ShortUUIDField(unique=True, length=10, max_length=20, prefix='INVENTORY',alphabet='abcdefgh12345' )    
    Name = models.CharField(max_length=100)
    Unit= models.CharField(max_length=100, default='Kilogram')
    Quantity = models.IntegerField()
    Updated =  models.DateTimeField(null=True, blank=True)
    
    class Meta:
         verbose_name_plural = "Product_Inventories"
    
    def __str__(self):
        return self.Name
    
    def get_quantity(self):
        return self.Quantity
    
    def modified_date(self):
        return self.Updated
    

class Product_Category(models.Model):
    """
    Categorizes products into logical groups for navigation and filtering (e.g., Electronics, Clothing).
    Includes a description and image for better UX.
    """
    
    ID_Product_Category= ShortUUIDField(unique=True, length=10, max_length=20, prefix='CAT',alphabet='abcdefgh12345')
    Name = models.CharField(max_length=100)
    #Desc= models.TextField(null=True, blank=True, default ='This is the discount')
    Desc= RichTextUploadingField(null=True, blank=True, default ='This is the discount')
    Image = models.ImageField(upload_to="category", default='category.jpg')
    
    class Meta:
         verbose_name_plural = "Product_Categories"
         
    def __str__(self):
        return self.Name
         
    def get_name(self):
        return self.Name
    
    def get_desc(self):
        return self.Desc
    

    
class Product(models.Model):
    """
    Represents a product available in the store. 
    Includes pricing, description, image, inventory reference, category, discount, and tags.
    """
    
    ID_Product= ShortUUIDField(unique=True, length =10, max_length=20, prefix="P", alphabet='abcdefgh12345') 
    Name = models.CharField(max_length=100)
    Desc= RichTextUploadingField(null=True, blank=True, default ='This is the product')
    Price = models.DecimalField(max_digits= 10, decimal_places=2, default="0")
    Cost = models.DecimalField(max_digits= 10, decimal_places=2, default="0")
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    inventory = models.ForeignKey(Product_Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Product_Category, on_delete=models.SET_NULL, null=True, blank=True, related_name= "category")
    Image = models.ImageField(upload_to = user_directory_path, default='product.jpg')
    Tags = TaggableManager(blank=True)
    Rating = models.IntegerField(choices=RATING, null=True, blank=True )
    
    class Meta:
        verbose_name_plural= 'Products'
    
    def __str__(self):
        return self.Name
    def product_image(self):
        return mark_safe('<img src="%s" width="50" heigh="50" />' % (self.Image))
    
    def get_price(self):
        if self.discount == None:
            return self.Price
        else:
            if self.discount.Active:
                return (1-self.discount.Discount_Percent)*self.Price
            return self.Price


class ProductImages(models.Model):
    """
    Stores additional images for a product, supporting multiple product views.
    Related to a single product.
    """
    
    images = models.ImageField(upload_to='product-image', default="product.jpg")
    product = models.ForeignKey(Product,related_name='p_images', on_delete=models.SET_NULL, null=True, blank=True)
    date= models.DateTimeField(auto_now_add=True)
    

################################### Order Management ################################

    
class Payment(models.Model):
    """
    Stores payment details for a user's order.
    Includes method, total amount, and description.
    """
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    ID_Payment= ShortUUIDField(unique=True, length=10, max_length=20, prefix="PAY")
    Desc= models.TextField(null=True, blank=True, default ='This is the payment')
    Date = models.DateTimeField(auto_now_add= True)
    Method= models.CharField(choices=PAYMENT_CHOICE,max_length=100, default="No")
    Money = models.DecimalField(max_digits= 10, decimal_places=2, default="0")
    
    class Meta:
        verbose_name_plural= 'Payment'
    
    def __str__(self):
        return self.ID_Payment
    
    
class Order_Detail(models.Model):
    """
    Represents an order placed by a user.
    Includes payment info, total price, delivery status, and optional note.
    """
    
    ID_Order_Detail = ShortUUIDField(unique= True, length=10, max_length=20, prefix="ORDER", alphabet='abcdefgh12345') 
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    Payment= models.ForeignKey(Payment,on_delete= models.SET_NULL, null=True)
    Date = models.DateTimeField(auto_now_add= True)
    Total_Price = models.DecimalField(max_digits= 10, decimal_places=2, default="0")
    Payment_Status = models.BooleanField(default=False)
    Delivery_Status = models.CharField(choices=STATUS_CHOICE, max_length=10, default='process')
    Note = models.TextField(null=True, blank=True, default ='Nothing')
    class Meta:
        verbose_name_plural= 'Order_Detail'
    
        
class Order_Item(models.Model):
    """
    Represents individual items within an order.
    Stores quantity, product reference, and subtotal for each item.
    """
    
    product =  models.ForeignKey(Product, on_delete= models.SET_NULL, null=True)
    order_detail= models.ForeignKey(Order_Detail, on_delete=models.SET_NULL, null=True)
    Quantity = models.IntegerField(default=1)
    Total = models.DecimalField(max_digits=999999, decimal_places=2, default='1.99')
    
    class Meta:
        verbose_name_plural= 'Order_Items'


    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.Image))




class Coupon(models.Model):
    """
    Represents a promo code or coupon that users can apply at checkout.
    Includes discount amount and active status.
    """
    
    Code = models.CharField(max_length=100)
    Discount = models.DecimalField(max_digits=10, decimal_places=2, default="0.1")
    Active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.Code


################################### Product Review, wishlists ################################


class ProductReview(models.Model):
    """
    Stores product reviews written by users.
    Includes star rating, rich text review content, and review date.
    """
    ID_ProductReview= ShortUUIDField(unique= True, length=10, max_length=20, prefix="REVIEW", alphabet='abcdefgh12345')
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    Review = RichTextUploadingField()
    Rating = models.IntegerField(choices=RATING, default=None)
    Date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural= "Product Reviews"   

    def __str__(self):
        return self.product.Desc
    
    def get_rating(self):
        return self.Rating
    

class Wishlist(models.Model):
    """
    Tracks products a user has favorited or saved for later.
    One entry per user-product combination.
    """
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    Date =models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural="Wishlists"
    
    def __str__(self):
        return self.product.Desc
    


    
    


########################### Staff Management ##########################



class Staff(models.Model):
    """
    Stores information about employees/staff members.
    Includes ID card number, birthday, job position, and start date.
    """
    
    ID_Staff = ShortUUIDField(unique=True, length =10, max_length=20, prefix="STAFF", alphabet='abcdefgh12345') 
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ID_card = models.CharField(max_length=20, null=False)
    Started = models.DateTimeField(null=True, blank=True)
    Birthday= models.DateTimeField(null=True, blank=True)
    Position= models.CharField(max_length=20,null=True)
    
    class Meta:
        verbose_name_plural= 'Staffs'
    
    
class Salary(models.Model):
    """
    Stores salary payment information for a staff member.
    Includes salary amount, bonus, and payment date.
    """
    
    ID_Salary = ShortUUIDField(unique=True, length =10, max_length=20, prefix="SALARY", alphabet='abcdefgh12345') 
    staff= models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    Date = models.DateTimeField(null=True, blank=True)
    Desc= models.TextField(null=True, blank=True, default ='This is a salary')
    Salary = models.DecimalField(max_digits=999999, decimal_places=2, default='1.99')
    Bonus = models.DecimalField(max_digits=999999, decimal_places=2, default='1.99')
    
    class Meta:
        verbose_name_plural= 'Salaries'
        


        
        


        
    
    










