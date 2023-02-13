from django.db import models

class UserDetail(models.Model):
    uname=models.CharField(unique=True, max_length=50)
    uemail=models.CharField(max_length=50)
    uphone=models.CharField(max_length=50, null=True)
    upassword=models.CharField(max_length=50)
    uactive=models.BooleanField(default=True)
    def __str__(self): 
        return self.uname 

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name      

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='imagestore/')
    stock = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='Wired')
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    cartid=models.AutoField(primary_key=True)
    user=models.ForeignKey(UserDetail, on_delete=models.CASCADE, null=False)

class CartItem(models.Model):
    cartitemid=models.AutoField(primary_key=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=False)
    quantity=models.PositiveBigIntegerField()
    def subtotal(self):
        return int(self.product.price)*int(self.quantity)

STATE_CHOICES = (
    ('KARNATAKA', 'KARNATAKA'),
    ('KERALA', 'KERALA'),
    ('TAMIL NADU', 'TAMIL NADU'),
    ('GOA', 'GOA'),
    ('GUJARAT', 'GUJARAT')
)
   
    
class Address(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    housename = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50, default='KERALA')
    selected = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Canceled', 'Canceled')
)
TYPE_CHOICES = (
    ('Cash on delivery', 'Cash on delivery'),
    ('UPI', 'UPI'),
    ('Razorpay', 'Razorpay'),
)
class Order(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordertype = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Cash on delivery')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
