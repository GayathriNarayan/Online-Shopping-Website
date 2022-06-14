from operator import truediv
from pickle import TRUE
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.timezone import now

class CustomerInfo(models.Model):
    '''
    Customer information
    username,password,first_name,last_name,email from default Users table
    One cutomer will have one information
    '''    
    customer=models.OneToOneField(User,on_delete=models.CASCADE)    
    address=models.CharField(max_length=255)
    phone=models.CharField(max_length=50)
    
    def __str__(self):
       return '{} {}'.format(self.user.first_name, self.user.last_name)

class ProductClassification(models.Model):
    '''
    Various Types of products
    '''    
    name = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=1000)
    
    def __str__(self):
       return '{} {}'.format(self.name, self.description)

class Product(models.Model):
    '''
    Product table which has a reference to the category and
    each category can have more than one product
    '''
    #Gender valriables   
    GENDER_F = 0
    GENDER_M = 1
    GENDER_CHOICES = [
        (GENDER_F, 'Female'),
        (GENDER_M, 'Male')
    ]   
  
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)    
    productclassification = models.ForeignKey(ProductClassification, on_delete=models.CASCADE)
    gender = models.IntegerField(choices=GENDER_CHOICES,blank=True,null=True)
    price =models.DecimalField(max_digits=10,
                                decimal_places=2,default=0)
    image=models.ImageField(upload_to='product_images',blank=True,default='default_product.jpg')                        

    def __str__(self):
       return '{} {}'.format(self.name, self.description)

class Size(models.Model):
    '''
    Various Types of sizes
    '''
    code=  models.CharField(max_length=50,blank=True,unique=True)  
    name = models.CharField(max_length=50)
    
    def __str__(self):
       return '{} {}'.format(self.code, self.name)

class ProductSize(models.Model):
    '''
    Various Types of sizes product wise
    '''  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)  

    '''
    A Product and a size together are unique
    '''
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'size'], name='product_size')
        ]

    def __str__(self):
       return '{} {}'.format(self.product.name, self.size.name)


class Order(models.Model):
    '''
    Order table which is the header table containing
    details of order reference number , order date, customer,payment details
    '''    
    order_reference = models.CharField(max_length=50,unique=True)
    order_date=models.DateTimeField(default=datetime.now)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.CharField(max_length=255)
    payment_provider=models.CharField(max_length=255)

    def __str__(self):
      return '{} {} {}'.format(self.order_reference, 
                                        self.order_date,
                                        self.customer)


class OrderDetail(models.Model):
    '''
    Order details table containing products ordered by a customer
    '''    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,null=True,blank=True)
    qty=models.IntegerField(default=0)
    price =models.DecimalField(max_digits=10,
                                decimal_places=2,default=0)
    image=models.CharField(max_length=255,null=True,blank=True)  
    
    def __str__(self):
       return '{} {} {} {} {} {}'.format(self.order.order_reference, 
                                        self.order.order_date,
                                        self.order.customer,
                                        self.product.name,
                                        self.qty,
                                        self.price)


 
class Product_Review(models.Model):
    '''
    Product Review table containing users reviews for a particular product 
    ''' 
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField(blank=True ,null=True)
    datetime = models.DateTimeField(default=now)
 
    def __str__(self):
        return '{} {}'.format(self.customer,self.content)