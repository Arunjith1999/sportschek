from email.policy import default
from django.db import models
#from login.models import CustomUser

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(blank= True)
    offer = models.IntegerField(default=0)



    class Meta:
        verbose_name_plural= 'categories'
    def _str_(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product',on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    image = models.ImageField(null = True, blank = True, max_length = 255000, upload_to = 'images/' ) 
    image2 = models.ImageField(null = True, blank = True, max_length = 255000, upload_to = 'images/')
    image3 = models.ImageField(null = True, blank = True,max_length= 255000, upload_to ='images/')  
    price = models.IntegerField(default=0)
    total_quantity = models.IntegerField( default = 0)   
    instock=models.BooleanField(default=True)
    offer = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Products'

        def __str__(self):
            return self.name      

    @property
    def get_offer_price(self):
            offer=int(self.offer)
            offer=offer-100
            offer_price = int(self.price) * int(offer)
            offer_price=offer_price/100
            offer_price=offer_price*-1
            return int(offer_price)
        
    @property
    def offer_category_price(self):
            offer = int(self.category.offer)
            offer=100-offer
            offer_price=(int(self.price)*offer)/100
            return int(offer_price)
        
    @property
    def final_price(self):
            if self.offer >= self.category.offer:
                offer=int(self.offer)
                offer=offer-100
                offer_price = int(self.price) * int(offer)
                offer_price=offer_price/100
                offer_price=offer_price*-1
                return int(offer_price)
            elif self.offer <= self.category.offer:
                offer = int(self.category.offer)
                offer=100-offer
                offer_price=(int(self.price)*offer)/100
                return int(offer_price)
            else:
                offer = int(self.category.offer)
                offer=100-offer
                offer_price=(int(self.price)*offer)/100
                return int(self.price)
                
        
    @property
    def product_offer(self):
            pro = self.offer
            return int(pro)
    @property
    def category_offer(self):
            cat = self.category.offer
            return int(cat)       



class Coupen(models.Model):
    coupon_code      =        models.CharField(max_length=10)
    is_expired       =        models.BooleanField(default=False)
    discount_price         =        models.IntegerField(default=100)
    minimum_amount   =        models.IntegerField(default=500)
    user             = models.ManyToManyField(to='login.CustomUser')
            
    def get_user(self):
        return self.user        



class user_coupon(models.Model):
    coupon = models.ForeignKey(Coupen,on_delete = models.CASCADE)
    user = models.ForeignKey(to='login.CustomUser',on_delete = models.CASCADE)       


# class product_offer(models.Model):
#     name = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
#     offer = models.IntegerField(default=0)    



# class category_offer(models.Model):
#     name = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
#     offer = models.IntegerField(default=0)  