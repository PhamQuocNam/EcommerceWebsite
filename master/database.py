from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe

# ============================
# 1. USER & PROFILE RELATED
# ============================

class User(models.Model):
    user_id = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.user.username} - {self.city}"


class Staff(models.Model):
    staff_id = ShortUUIDField(primary_key=True)
    staff_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    started_date = models.DateField()
    id_card = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Staffs'

    def __str__(self):
        return self.staff_name


# ============================
# 2. PAYMENT & SALARY
# ============================

class Payment(models.Model):
    payment_id = ShortUUIDField(primary_key=True)
    description = models.TextField()
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Payments'

    def __str__(self):
        return str(self.payment_id)


class Salary(models.Model):
    salary_id = ShortUUIDField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    salary_desc = models.TextField()
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    bonus = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Salaries'

    def __str__(self):
        return str(self.salary_id)


# ============================
# 3. PRODUCT & CATEGORY & INVENTORY
# ============================

class Discount(models.Model):
    discount_id = ShortUUIDField(primary_key=True)
    discount_name = models.CharField(max_length=255)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name_plural = 'Discounts'

    def __str__(self):
        return self.discount_name


class ProductCategory(models.Model):
    category_id = ShortUUIDField(primary_key=True)
    category_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories')
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Product Categories'

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_id = ShortUUIDField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    # Note: Inventory is managed in ProductInventory below

    class Meta:
        verbose_name_plural = 'Products'

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')

    def __str__(self):
        return self.product_name


class ProductInventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    quantity = models.IntegerField()
    modified_date = models.DateField()

    class Meta:
        verbose_name_plural = 'Product Inventories'

    def __str__(self):
        return str(self.product)


# ============================
# 4. ORDERING & WISHLIST & REVIEW
# ============================

class Wishlist(models.Model):
    wishlist_id = ShortUUIDField(primary_key=True)
    id_card = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return str(self.wishlist_id)


class OrderDetail(models.Model):
    order_detail_id = ShortUUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    order_date = models.DateField()
    total_money = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    delivery_status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Order Details'

    def __str__(self):
        return str(self.order_detail_id)


class OrderItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    order_detail = models.OneToOneField(OrderDetail, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    note = models.TextField()

    class Meta:
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.order_detail} - {self.product}"


class Review(models.Model):
    review_id = ShortUUIDField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    review_date = models.DateField()

    class Meta:
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"