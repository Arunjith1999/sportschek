from typing import OrderedDict
from django.db import models
from django.core import validators
from django.db.models import Q
#from.validation import validate_email

# Create your models here.
from email.policy import default
from enum import unique
#from tkinter import Widget
from django import forms
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models
from superuser.models import Product,Coupen
#from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self,first_name,last_name,username, email,phone, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name,last_name=last_name,username=username,email=email,phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,first_name,last_name,username ,email,phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_admin',False)
        extra_fields.setdefault('is_active',True)
        return self._create_user(first_name,last_name,username,email,phone, password, **extra_fields)

    def create_superuser(self,first_name,last_name,username, email,phone, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(first_name,last_name,username,email,phone, password, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=200, unique=True)
    # phone_regex = RegexValidator(regex =r'^\+?1?\d{9.14}$',message='Phone number must be entered in the format +919999999999. Up to 10 digits allo ')
    phone = models.CharField(max_length=50,unique=True)
    

    
    date_joined             = models.DateTimeField(auto_now_add=True,)
    last_login              = models.DateTimeField(auto_now_add=True)
    is_admin                = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_superuser            = models.BooleanField(default=False)

    def _str_(self):
        return self.username

    objects                  = CustomUserManager()
    USERNAME_FIELD          = 'email'
    REQUIRED_FIELDS         = ['first_name', 'last_name', 'phone', 'username']

    class Meta:
        verbose_name        = 'CustomUser'
        verbose_name_plural = 'CustomUsers'

    # def  validate_email(value):
    #     if '@gmail.com' in value:
    #         return value
    #     else:
    #         raise validators("enter the email in pro format")

          

class CustomerAddress(models.Model):
    user            = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    name               =models.CharField(max_length=200,null=True)
    phone_number      = models.CharField(max_length=99,null=True)
    house_name              = models.CharField(max_length=200, null=True)
    street_name             = models.CharField(max_length=200, null=True)
    city                    = models.CharField(max_length=200, null=True)
    state                   = models.CharField(max_length=200, null=True)
    country                 = models.CharField(max_length=200, null=True)
    Zip_code               = models.IntegerField(null=True)
    default_address         = models.BooleanField(default=False)

    def _str_(self):
        return str(self.user)







class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField(default=1)
    created_at =models.DateTimeField(auto_now_add=True)
    coupon=models.ForeignKey(Coupen,on_delete=models.SET_NULL,null=True,blank=True)
    is_paid=models.BooleanField(default=False)

    def get_cart_total(self):
        product = self.product
        quantity = self.product
        price = self.product.final_price
        return price*quantity
        
    def get_coupon_code(self):
        return None

class Address(models.Model):
    user            = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null = True)
    name       = models.CharField(max_length=200,null = True)
    phone_number    = models.CharField(max_length=99,null = True)
    house_name      = models.CharField(max_length=200, null = True)
    street_name      = models.CharField(max_length=200, null = True)
    landmark      = models.CharField(max_length=200, null = True)
    city            = models.CharField(max_length=200, null = True)
    default_address         = models.BooleanField(default=False)
    pin_code       = models.IntegerField( null = True)


class OrderTable(models.Model):
         
    COD = 'COD'
    RAZORPAY = 'RAZORPAY'
    PAYPAL = 'PAYPAL'
    
    PAYMENT_METHOD=[
   
        
        (COD, 'Cash On Delivery'),
        (RAZORPAY, 'Razor Pay'),
        (PAYPAL, 'Paypal')
    ]

    user            = models.ForeignKey(CustomUser,on_delete= models.CASCADE, null = True ,blank = True )
    amount          = models.FloatField(default=0)
    is_paid         = models.BooleanField(default=False)
    order_id        = models.CharField(max_length = 100, blank=True)
    payment_method  = models.CharField(max_length=100,choices = PAYMENT_METHOD, default=COD)
    payment_id      = models.CharField(max_length=100, blank=True)

    name            = models.CharField(max_length=100, blank=True)
    phone_number    = models.CharField(max_length=100, blank=True)
    house_name      = models.CharField(max_length=100, blank=True)
    street_name     = models.CharField(max_length=100, blank=True)
    city            = models.CharField(max_length=100, blank=True)
    state           = models.CharField(max_length=100, blank=True)
    country         =models.CharField(max_length=100,  blank=True)
    pin_code         = models.CharField(max_length=100, blank=True)
    orderstatus = [
        ('Pending', 'Pending'),
        ("Confirmed", 'Confirmed'),
        ("Delivered", "Delivered"),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected')
    ]
    report=[
        ('daily','daily'),
        ('weekly','weekly'),
        ('annually','annually')
    ]
    status          = models.CharField(max_length=100, choices = orderstatus, default='Pending')
    message         = models.TextField(null = True)
    created_at      = models.DateTimeField(auto_now_add=True)
    tracking_no     = models.CharField(max_length=100, default='none')
    date_delivered  = models.DateField(auto_now_add= False,choices=report,default='2022-01-01')    
    coupon          =models.ForeignKey(Coupen,on_delete=models.CASCADE,null=True,blank=True)
        
        
class OrderItem(models.Model):
    order           = models.ForeignKey(OrderTable, on_delete=models.CASCADE)    
    product_name    = models.CharField(max_length=100, blank=True)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    price           = models.IntegerField(null=False)
    quantity        = models.IntegerField(null=False)   

    def get_product_image(self):
        return (self.product.image)

    def get_name(self):
        return self.product.name


class Wallet(models.Model):
    
    Balance                 = models.IntegerField(default=0)
    
    user                    = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)


class WalletTransactions(models.Model):
    wallet                  = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True ) 
    amount                  = models.IntegerField(default=0)    
    user                    = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    CREDIT = 'CREDIT' 
    DEBIT = 'DEBIT'
    
    
    
    
    PAYMENT_METHOD=[
   
        
        (CREDIT, 'CREDIT'),
        (DEBIT, 'DEBIT'),
        
    ]
    
    status                  = models.CharField(max_length=100,choices = PAYMENT_METHOD, null=True)        