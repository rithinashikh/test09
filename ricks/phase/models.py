from django.db import models

class UserDetail(models.Model):
    uname=models.CharField(unique=True, max_length=50)
    uemail=models.CharField(max_length=50)
    uphone=models.BigIntegerField(default=None)
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
