import email
from itertools import product
import random
from .forms import CustomerProfileForm
# from tkinter import *
# from tkinter import messagebox
from unicodedata import name
from superuser.models import Category
from superuser.models import Product
from django.shortcuts import render
from django.contrib.auth.models import auth
from django.views import View
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import auth
from.models import CustomUser as User,Cart,OrderTable,OrderItem,CustomerAddress,Coupen,Address,Wallet,WalletTransactions
from.mixins import MessageHandler
from . import verify
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,EmptyPage
from django.http import JsonResponse
# from .forms import VerifyForm

# Create your views here.
def userlogin(request):
  if 'user_id' in request.session:
      return redirect(home)
    

  if    request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        if user is not None:
        
            request.session['user_id'] = email
            login(request,user)
            print(user)
            return redirect(home)
        
        else:
            messages.error(request,("Incorrect email id or Password,Try again.."))
            return redirect(userlogin)
  else:   
        return render (request,'authenticate/login.html',{})



def register(request):
    if 'user_id'in request.session:
        return redirect(home)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        phone=request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
       
        if password1 == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request,"email already exists")
                return redirect('register')
            elif (len(phone) > 12) :
                messages.info(request,"enter valid phone number")
                return redirect('register')
            elif ((first_name == '')|(last_name == '')|(username == '')|(password1 == '')|(email == '')|(phone == '')):
                messages.info(request,"All fields are mandatory")    
                return redirect('register')
            elif User.objects.filter(phone = phone).exists():
                messages.info(request,"number already used")
                return redirect('register')    
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,phone=phone,first_name=first_name,last_name=last_name)
                user.save()
                messages.success(request,"user registered succesfully")
                return redirect('login')
        else:
            messages.error(request,"Password are not matching")
            return redirect('register')

        
    else:
        return render(request,"authenticate/register.html")





def home(request):
    if 'user_id' in request.session: 
        products=Product.objects.all()
        customer_obj=User.objects.get(email=request.session['user_id'])
        customer=customer_obj
        log=True
        cate=Category.objects.all()   
        return render (request,'authenticate/home.html',{'products':products,'cate':cate,'customer':customer,'log':log})    
    else:
        cate=Category.objects.all()  
        products=Product.objects.all()
        log=False
        return render(request,'authenticate/home.html',{'products':products,'cate':cate,"log":log})


# def forget(request):
#     if request.method == 'POST':
#         email=request.POST['email']
#         phone=request.POST['phone']
#         user = User.objects.get(email=email, phone=phone)
#         user=authenticate(request,email = email,phone = phone)
#         if user is not None:
#             return redirect ('otp')
#         else:
#             messages.error(request,'Number is not registered or invalid email')  
#             return redirect('login')
#     else:          
#         return render(request,'authenticate/forget.html')

def otp_login(request):
   
    if request.method == 'POST':
        phone = request.POST['phone_number']
        #p=User.objects.filter(phone=phone)
        if  len(phone)!=10:
            messages.error(request, 'invalid Credentials')
        else:
            account_obj = User.objects.get(phone=phone)
            global account_
            def account_():
                return phone

            if account_obj:
               
                otp = random.randint(1000, 9999)
                
                message_handler = MessageHandler(('+91'+phone),otp).send_otp_on_phone()
                global otp_id
                def otp_id():
                    return otp
                return redirect(otp_confirm)
                
       
    return render(request, 'Authenticate/otp_login.html')

def otp_confirm(request):
    phone = None
    
    if request.method == "POST":
        otp_number = request.POST['otp']
      
        if int(otp_number) == int(otp_id()):
            
            
            phone = account_()
            user = User.objects.filter(phone=phone)
            email=user[0].email
            request.session['user_id'] = email
            return redirect(home)
            #print(email)

            # password = user[0].password
            # print(password)
            # user = authenticate(request, username=email, password=password)
            # print(user)
            
        else:
            messages.error(request, 'Otp invalid')
            
            return redirect(otp_confirm)
    user = User.objects.filter(phone=phone)   
    return render(request, 'Authenticate/otp.html',{'user':user})
def userlogout(request):
    request.session.flush()
    logout(request)
    return redirect(userlogin)

def shop(request):
    if 'user_id' in request.session:
        global e
        e=10
        products = Product.objects.all()
        customer_obj = User.objects.get(email=request.session['user_id'])
        customer= customer_obj.id
        cat = Category.objects.all()
        return render(request, 'user/shop.html', {'products':products, "cat":cat, 'customer':customer},)
    else:
        return redirect(userlogin)




def view_product(request,id):
    # if 'user_id' in request.session:
    #     return redirect(home)
    products=Product.objects.filter(id=id)
    
    
    return render(request,'authenticate/product_view.html',{'products':products})





def cartview(request):
   
           if 'user_id' in request.session:
                
                user=User.objects.get(email=request.session['user_id'])
                cart=Cart.objects.filter(user=user).order_by('created_at')
                # cust=CustomerAddress.objects.filter(user= user)
                # cust[0].default_address = True
                # cust[0].save()
                try:
                    address = CustomerAddress.objects.get(default_address = True, user= user)
                except:
                    address = None
                cartloop=Cart.objects.filter(user=user).values()
                category = Category.objects.all()
                total_sum=0
                sum = 0
                for i in cartloop:
                    product_id=i['product_id']
                    quantity=i['quantity']
                    product_obj=Product.objects.get(id=product_id)
                    # product_queryset=product_obj[0]
                    # product_price=product_queryset['price']
                    # total=product_price*quantity
                    total_sum=total_sum+(product_obj.final_price)*quantity
                print(total_sum)
                total=int(total_sum)
                try:
                    coupon_available=Coupen.objects.get(id=cart[0].coupon_id)
                except:
                    coupon_available=None

                if coupon_available:
                    offer_with_coupon = total-coupon_available.discount_price
                else:
                    offer_with_coupon = None   
                log=True             
                if total_sum==0:
                    return render(request,'authenticate/empty_cart.html') 
                return render(request,'authenticate/cart.html',{'log':log,'cart':cart,'total':total,'category':category,'coupon_available':coupon_available,'offer_with_coupon':offer_with_coupon,'address':address})  
           else:
                log:False
                try:
                    cart = request.session['cartdata']
                except:
                    cart=None
                total_amt=0
                if'cartdata' in request.session:
                    for p_id,item in request.session['cartdata'].items():
                        total_amt+=int(item['qty'])*int(item['price'])
                    id=str(11)
                    

                    return render(request,'authenticate/guest_cart.html',{'data':request.session['cartdata'],'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})            
                else:
                    return render(request,'authenticate/guest_cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})

    #     return redirect(userlogin)       


def add_cart(request,id):
    if 'user_id' in request.session:
        print('hy add')
        product_id=id

        user_obj = User.objects.get(email=request.session['user_id'])
        user_id =  user_obj.id
        obj = Cart.objects.filter(product_id=product_id, user_id=user_id)


        if obj:
            product_query_obj = obj[0]
            current_quantity = product_query_obj.quantity
            #  current_quantity=current_quantity+1
            # cart = Cart.objects.get(product_id=product_id,user_id=user_id)
            # cart.quantity=current_quantity
            # cart.save()
            # return HttpResponse('')
            total_quantity=product_query_obj.product.total_quantity
            if total_quantity>0 and total_quantity>current_quantity:
                current_quantity = current_quantity+1
                cart = Cart.objects.get(product_id=product_id,user_id=user_id)
                cart.quantity=current_quantity
                cart.save()
            return HttpResponse('')    
        else:
            cart = Cart.objects.create(product_id=product_id,user_id=user_id)
            cart.save()
            return HttpResponse('')

    else:
        product = Product.objects.get(id=id)
        cart_p={}
        cart_p[str(id)]={
            'image':str(product.image),
            'name':product.name,
            'price':product.price,
            'qty':int(1),}
        if 'cartdata' in request.session:
            if str(id) in request.session['cartdata']:
                cart_data=request.session['cartdata']
                cart_data[str(id)]['qty']=int(cart_p[str(id)]['qty'])
                cart_data.update(cart_data)
                request.session['cartdata']=cart_data
            else:
                cart_data=request.session['cartdata']
                cart_data.update(cart_p)
                request.session['cartdata']=cart_data
        else:
            request.session['cartdata']=cart_p
            
        print(cart_p)    
        return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})
        



def add_cart_product_view(request,id):
    if 'user_id' in request.session:
        product_id=id
        user_obj=User.objects.get(email=request.session['user_id'])
        user_id=user_obj.id
        obj =Cart.objects.filter(product_id=product_id,user_id=user_id)   

        if obj:
            product_query_obj= obj[0]
            current_quantity=product_query_obj.quantity
            current_quantity=current_quantity+1
            cart= Cart.objects.get(product_id=product_id,user_id=user_id)
            cart.quantity=current_quantity
            cart.save()
            return HttpResponse('')

        else:
            cart = Cart.objects.create(product_id=product_id,user_id=user_id)
            cart.save()
            return HttpResponse('')
    else:
        return redirect(userlogin)



def delete_cart(request):
    cart=Cart.objects.all()
    cart.delete()
    return redirect (cartview)

def delete_product_cart(request,id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    return redirect(cartview)


def increment_cart_quantity(request,quantity,id):
    cart_obj=Cart.objects.filter(id=id)    
    product_query_obj = cart_obj[0]
    
    product = product_query_obj.product
    current_quantity=product_query_obj.quantity
    product_id=product.id
    # print(product_id)
    # print(quantity)
    # print(id)
    if product.total_quantity>0 and current_quantity< product.total_quantity  :
        #=========== cart stock increment==========
        current_quantity=product_query_obj.quantity
        current_quantity=current_quantity+1
        print(current_quantity)
        cart_obj.quantity =current_quantity
        # print(cart_obj.quantity)
        Cart.objects.filter(id=id).update(quantity=current_quantity)
       
        return HttpResponse('success')


    else:

        return HttpResponse('success')

def update_quantity(request,id):
    quantity=id
    return HttpResponse('success')

def decrement_cart_quantity(request,quantity,id):
    cart_obj= Cart.objects.filter(id=id)
    product_query_obj = cart_obj[0]
    current_quantity = product_query_obj.quantity
    product = product_query_obj.product
    product_id=product.id


    if current_quantity >1:
        #======cart stock deincrement =======
        cart_obj = Cart.objects.filter(id=id)
        #current_quantity=product_query_obj.quantity
        product_query_obj = cart_obj[0]
        current_quantity= product_query_obj.quantity
        current_quantity= current_quantity-1
        print(current_quantity)
        cart_obj.quantity = current_quantity
        Cart.objects.filter(id=id).update(quantity=current_quantity)
       

        return HttpResponse('success')

    else:
        return HttpResponse('success')



#==============ORDER MANAGEMENT============


def checkout(request):
    # if 'user_id' in request.session:
    if request.user.is_authenticated:
        user=User.objects.get(email=request.session['user_id'])
        try:
                address = CustomerAddress.objects.filter(user_id=user.id)
                address_query=address[0]

        except:
                address=None

        return render(request,'authenticate/checkout.html',{'address':address})
    else:
        return redirect(userlogin)    
    # else:
    #     return render(userlogin)    
        
def userprofile(request):
    category = Category.objects.all()
    if 'user_id' in request.session:
        user=User.objects.get(email=request.session['user_id'])
        address=CustomerAddress.objects.filter(user_id=user.id)
        try:
            wallet=Wallet.objects.get(user=user)
        except:
            wallet=None    
        return render(request,'authenticate/profile.html',{'user':user,'category':category,'address':address,'wallet':wallet})
    
    # if 'user_id ' in request.session:
    #     return render(request,'authenticate/profile.html')

    else:
         return redirect(userlogin)

def add_address(request):
    
        print('hello')
        if request.method == 'POST':
            user = User.objects.get(email=request.session['user_id'])
            name = request.POST['name']
            phone_number=request.POST['phone']
            house_name=request.POST['house_name']
            street_name= request.POST['street_name']
            city=request.POST['city']
            state=request.POST['state']
            country=request.POST['country']
            Zipcode=request.POST['Zipcode']

            # phone_number_obj = CustomerAddress.objects.filter(phone_number=phone_number)
            # if phone_number_obj:
            #     print('hi1')
            #     messages.error(request, 'credentials invalid')

            if len(phone_number)!=10:
                print('hi2')
                messages(request, 'credentials INvalid')

            elif len(Zipcode)!=6:
                print('hi3')
                messages.error(request,'credentials invalid')

            else:
                print('hi4')
                CustomerAddress.objects.create(user=user,name=name,phone_number=phone_number,house_name=house_name,street_name=street_name,city=city,state=state,country=country,Zip_code=Zipcode)    
                messages.success(request,'Address added Successfully')


        return render(request,'authenticate/add_address.html')        

            
def choose_address_select(request):

    if "user_id" in request.session: 
        user = User.objects.get(email=request.session['user_id'])
        try:
            address= CustomerAddress.objects.filter(user_id=user.id)
            address_query=address[0]

        except:
            address= None 

        return render(request,'authenticate/checkout.html',{'address':address})       
        
    else:
        return redirect(userlogin)   

def choose_address(request):
    if request.method == 'POST':
            address_id = request.POST['address']
            global check_out_address
            def check_out_address():
                return address_id

            Address.objects.all().update(default_address=False)
            address = CustomerAddress.objects.get(id=address_id)
            address.default_address = True
            address.save()
            return redirect(cartview)    

            
    else:
        return redirect(userlogin)       




def choose_payment_method(request,id):
    if "user_id" in request.session: 
        user = User.objects.get(email=request.session['user_id'])
        cart=Cart.objects.filter(user=user).order_by('created_at')
        cartloop = Cart.objects.filter(user=user).values()

        total_sum=0
        for i in cartloop:
            product_id=i['product_id']
            quantity=i['quantity']
            product_obj=Product.objects.get(id=product_id)
       
            total_sum=total_sum+(product_obj.final_price)*quantity
        
        total=total_sum

        # global total_amount
        # def total_amount():
        #     return total
        print(f'helloooooooooooooooooooooooooooooooooooo{id}')
        address = CustomerAddress.objects.filter(user=user, id=id)    
        cart =Cart.objects.filter(user=user).order_by('created_at')
        try:
            coupon_available=Coupen.objects.get(id=cart[0].coupon_id)
        except:
            coupon_available=None
        if coupon_available:
            offer_with_coupon = total-coupon_available.discount_price
        else:
            offer_with_coupon = total                
        return render(request, 'authenticate/payment_method.html', {'address':address, 'address_id':id, 'cart_total':total,'coupon_available':coupon_available,'offer_with_coupon':offer_with_coupon}, )
    else:
        return redirect(userlogin)   
    
def update_address(request, id):
    if "user_id" in request.session: 
        # form = CustomerForm()
        # context = {'form':form}
        print(messages)
        if request.method == 'POST':
            user = User.objects.get(email=request.session['user_id'])  
            name = request.POST['name']
            phone = request.POST['phone']
            house_name = request.POST['house_name']
            street_name = request.POST['street_name']
            landmark = request.POST['landmark']
            city = request.POST['city']
            pin  = request.POST['pin']

        
            if len(phone)!=10:
                messages.error(request, 'Credentials invalid')
            # elif  len(phone)!=10 :
            #     messages.error(request, 'Credentials invalid')


            elif  len(pin)!=6:
                messages.error(request, 'Credentials invalid')   
            else:

                CustomerAddress.objects.filter(id=id).update( user=user, name=name, phone_number=phone,house_name=house_name, street_name=street_name, landmark=landmark, city=city, pin_code=pin)  
                messages.success(request, 'Address Updated successfully') 
    address=CustomerAddress.objects.get(id=id)   
            
    return render(request, 'authenticate/update_address.html', {'item':address})    


def update_address_user(request, id):
    if "user_id" in request.session: 
        # form = CustomerForm()
        # context = {'form':form}
        print(messages)
        if request.method == 'POST':
            user = User.objects.get(email=request.session['user_id'])  
            name = request.POST['name']
            phone = request.POST['phone']
            house_name = request.POST['house_name']
            street_name = request.POST['street_name']
            landmark = request.POST['landmark']
            city = request.POST['city']
            pin  = request.POST['pin']

            
            
            if  len(phone)!=10 :
                messages.error(request, 'Cedentials invalid')


            elif  len(pin)!=6:
                messages.error(request, 'Cedentials invalid')   
            else:

                CustomerAddress.objects.filter(id=id).update( user=user, name=name, phone_number=phone,house_name=house_name, street_name=street_name, landmark=landmark, city=city, pin_code=pin)  
                messages.success(request, 'Address Updated successfully') 
            address=Address.objects.get(id=id)   
                    
            return render(request, 'authenticate/update_address_user.html', {'item':address, 'address_id':id})   
    else:
        return redirect(userlogin) 

def delete_address_user(request,id):
    if "user_id" in request.session: 
        user = CustomerAddress.objects.get(id=id)
        user.delete()  
        return redirect(userprofile)
    else:
        return redirect(userlogin) 

def choose_payment(request):
    if "user_id" in request.session: 
      
        if request.method == 'GET':
            payment_method = request.GET['optradio']
            amount = request.GET['cart_total']
            if payment_method == 'RAZORPAY':
                return redirect('razorpay_pay',amount)
            elif payment_method == 'COD':
                return redirect('create_order', 1)
            elif payment_method == 'PAYPAL':
                return redirect('paypal', amount)
            else:
                return redirect(home)


def create_order(request,id):
    if "user_id" in request.session: 
        
            
            if id == 1:
                payment_method = 'COD'
                is_paid = False
            elif id == 3:
                payment_method = 'PAYPAL'
                is_paid = True
            elif id == 2:
                payment_method = 'RAZORPAY'
                is_paid = True
                    
            user = User.objects.get(email= request.session['user_id'])
            address = CustomerAddress.objects.get(default_address=True,user=user)
            cart =Cart.objects.filter(user=user).order_by('created_at')
            cartloop = Cart.objects.filter(user=user).values()

            total_sum=0
            for i in cartloop:
                product_id=i['product_id']
                quantity=i['quantity']
                product_obj=Product.objects.get(id=product_id)
                total_sum = total_sum+(product_obj.final_price)*quantity

            amount = total_sum    
             
            name = address.name
            phone_number = address.phone_number
            house_name = address.house_name
            street_name = address.street_name
            city =address.city
            state=address.state
            country=address.country
            zip_code = address.Zip_code
            tracking_no = str(user)+str(random.randint(1111111,9999999))
            while OrderTable.objects.filter(tracking_no=tracking_no) is None:
                tracking_no = user+str(random.randint(1111111,9999999))
            tracking_no=tracking_no

            try:
                coupon_available = Coupen.objects.get(id=cart[0].coupon_id)
            except:
                coupon_available=None
            if coupon_available:  
                amount = int(amount)-int(coupon_available.discount_price)      
                order = OrderTable.objects.create(user=user, amount=amount, payment_method=payment_method,
                                    name=name,phone_number=phone_number,house_name=house_name, 
                                    street_name=street_name, city=city,state=state,country=country,pin_code=zip_code,
                                    tracking_no=tracking_no,coupon=coupon_available,is_paid=is_paid)
            else:
                order = OrderTable.objects.create(user=user, amount=amount, payment_method=payment_method,
                                    name=name,phone_number=phone_number,house_name=house_name, 
                                    street_name=street_name, city=city,state=state,country=country,pin_code=zip_code,
                                    tracking_no=tracking_no,coupon=coupon_available,is_paid=is_paid)

            # global order_id
            # order_id=order.id
            # def order_id():
            #     return order.id




           
            ordr_query = OrderTable.objects.get(tracking_no=tracking_no)
            
            cart = Cart.objects.filter(user=user)
            for cart in cart:
                item_quantity = cart.quantity
                product = Product.objects.get(id = cart.product_id)
                print(item_quantity, product)
                OrderItem.objects.create(order=ordr_query, product_name=product.name, product=product, price=product.price, quantity=item_quantity)
                item_quantity=product.total_quantity-item_quantity
                Product.objects.filter(id = cart.product_id).update(total_quantity=item_quantity)
                if item_quantity < 1:
                    Product.objects.filter(id = cart.product_id).update(instock=False)
                elif item_quantity >= 1:
                    Product.objects.filter(id = cart.product_id).update(instock=True)

                cart.delete() 
            return redirect(payment_success_page)     
        # if payment_method == 'RAZORPAY':
        #     print('hiii')
        #     return redirect(razorpay_pay)
        # elif payment_method == 'PAYPAL':
        #     return redirect(paypal)
        # else:
        #     return redirect(home)

        
    return redirect(userlogin)

def payment_success_page(request):
    if "user_id" in request.session:
        return render(request,'authenticate/payment_success.html')
    else:
        return redirect(userlogin)       

def order_user(request):
    category = Category.objects.all()
    if "user_id" in request.session: 
        order=OrderTable.objects.all().order_by('created_at').values()
        p=Paginator(order, 10)
        page_num = request.GET.get('page',1)
        
        try:
            
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
       
      
        return render(request, 'authenticate/order_user.html', {'order':page,'category':category,} )
    else:
        return redirect(userlogin)   

def order_products(request,id):
    if 'user_id' in request.session:
        #product = Product.objects.get(id=id)
        order_obj = OrderItem.objects.filter(order_id=id)
        print(id)
        print(order_obj)


        return render(request,'authenticate/order_products.html',{'p':order_obj})


def active_orders(request):
    
    if "user_id" in request.session: 
        order=OrderTable.objects.filter(Q(status='Confirmed')|Q(status='Pending')).order_by('created_at').values()
        products = OrderItem.objects.all()
        p=Paginator(order,10)
        page_num=request.GET.get('page',1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page=p.page(1)    
       
        return render(request, 'authenticate/active_orders.html', {'order':page}, )
    else:
        return redirect(userlogin)

def active_order_products(request,id):
    if 'user_id' in request.session:
        OrderTable.objects.filter(status='Confirmed').order_by('created_at').values()
        products = OrderItem.objects.filter(order_id=id)

        for item in products:
            product=Product.objects.get(id=item.product_id)
            quantity=item.quantity

        return render(request,'authenticate/active_order_products.html',{'products':products})  
    else:
        return redirect(userlogin)    

def delivered_orders(request):
    if "user_id" in request.session: 
        order=OrderTable.objects.filter(status='Delivered')
        
        p=Paginator(order, 10)
        page_num = request.GET.get('page',1)
        
        try:
            
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
          
       
        
        return render(request,'authenticate/delivered_orders.html',{'order':page} )
    else:
        return redirect(userlogin)
def return_order(request,id):
    if "user_id" in request.session: 
        pass
        order_products = OrderItem.objects.filter(order_id=id).order_by('created_at')
        order=OrderTable.objects.get(id=id)
       
        
        
            
        print(order.amount)
       
        return redirect(delivered_orders)
    else:
            return redirect(userlogin)

def order_cancel_user(request,id):
    if 'user_id' in request.session:
        OrderTable.objects.filter(id=id).update(status='Canceled')
        order_products=OrderItem.objects.filter(order_id=id)

        for item in order_products:
            product=Product.objects.get(id=item.product_id)  
            quantity=item.quantity
            if product.total_quantity == 0:
                    
                    product.total_quantity=product.total_quantity+quantity
                    product.instock = True
                    product.save()
                
            else:
                    
                    product.total_quantity=product.total_quantity+quantity
        return redirect(active_orders)    

    else:
        return redirect(userlogin)

        
                    
# def guest_user(request):
#     products=Product.objects.all()
#     cate=Category.objects.filter(name=name)
#     return render(request,'authenticate/guest_home.html',{'products':products,'cate':cate})     


# def guest_cart(request):
#         cart=Cart.objects.order_by('created_at')
#         print('gh')
#         cartloop=Cart.objects.values()

#         total_sum=0
#         for i in cartloop:
#             product_id=i['product_id']
#             quantity=i['quantity']
#             product_obj=Product.objects.filter(id=product_id).values()
#             product_queryset=product_obj[0]
#             product_price=product_queryset['price']
#             total=product_price*quantity
#             total_sum=total_sum+total
#         print(total_sum)

#         total=total_sum
#         global sub_total
#         def sub_total():
#             return total
#         print(total)
#         return render(request,'authenticate/cart.html',{'cart':cart,'total':total})      

# def guest_add_cart(request):
#     product_id=id
#     obj = Cart.objects.filter(product_id=product_id)

#     if obj:
#            product_query_obj = obj[0]
#            current_quantity = product_query_obj.quantity
#            current_quantity=current_quantity+1
#            cart = Cart.objects.get(product_id=product_id)
#            cart.quantity=current_quantity
#            cart.save()
#            return HttpResponse('')     
#     else:
#            cart = Cart.objects.create(product_id=product_id)
#            cart.save()
#            return HttpResponse('')        
       
def razorpay_pay(request,amount):
    if "user_id" in request.session:
            print('hi')
            # order=OrderTable.objects.get(id=order_id())
            # OrderTable.objects.filter(id=order_id()).update(is_paid=True)
            user=User.objects.get(email=request.session['user_id'])
            cart=Cart.objects.filter(user=user).order_by('created_at')
            try:
                coupon_available=Coupen.objects.get(id=cart[0].coupon_id)
            except:
                coupon_available=None

            if coupon_available:
                amount = int(amount)- int(coupon_available.discount_price)
            else:
                amount = amount             

            import razorpay
            client = razorpay.Client(auth=("rzp_test_xCvV0RihrwVFik", "CJcWxRCWF0yDuCla7DzzG5HY"))
            DATA = {
                    "amount": ((amount)*100),
                    "currency": "INR",
                        "receipt": "receipt#1",
                        # "notes": {
                        #     "key1": "value3",
                        #     "key2": "value2"
                        # }
            }
            razor_order=client.order.create(data=DATA)
            razor_id=razor_order['id']
                    
            return render(request,'authenticate/razorpay.html',{'order_id':razor_id,"order_amount":amount,'user':user})    
    else:
        return redirect(userlogin)    

@csrf_exempt
def razorpay_success(request):
    if 'user_id' in request.session:
        return redirect('create_order',2)
    else:
        return redirect(userlogin)    


def paypal(request,amount):
    if 'user_id' in request.session:
        user = User.objects.get(email = request.session['user_id'])
        cart = Cart.objects.filter(user=user).order_by('created_at')
        try:
            coupon_available=Coupen.objects.get(id=cart[0].coupon_id)
        except:
            coupon_available=None
        if coupon_available:
            amount = int(amount)-int(coupon_available.discount_price)
        else:
            amount=amount
            return render(request, 'authenticate/paypal.html',{"order_amount":amount, 'user':user})           
    #     order=OrderTable.objects.get(id=order_id())
    #     OrderTable.objects.filter(id=order_id()).update(is_paid=True)
    #     user=User.objects.get(email=request.session['user_id'])
    #     return render(request,'authenticate/paypal.html',{'order':order, 'order_amount':order.amount,'user':user})
    else:
        return redirect(userlogin)


def paypalsuccess(request):
    if 'user_id'in request.session:
        return render(request,'authenticate/payment_success.html')

    else:
        return redirect(userlogin)   

def apply_coupon(request,id):
    from superuser.models import user_coupon
    
    if "user_id" in request.session: 
        
        coupon_code = request.GET['coupon_code']
        try:
            coupon= Coupen.objects.get(coupon_code=str(coupon_code))
        except:
            coupon=None    
        user = User.objects.get(email=request.session['user_id'])
        cart = Cart.objects.filter(user=user)
        cartloop = Cart.objects.filter(user=user).values()
        cu =Coupen.objects.all()
        try:
            user_coupon_obj = user_coupon.objects.get(coupon=coupon, user=user)
        except:
            user_coupon_obj = None
        #print(customer)
       
        # cou = Coupen.objects.get(user=customer)
        # print(f'ehhehehehhehehhehehehehhehe {cou}')
        total_sum=0
        for i in cartloop:
            
        #===========================================================    
            product_id=i['product_id']
            quantity=i['quantity']
            product_obj=Product.objects.get(id=product_id)
            
            #print(product_obj.final_price)
            
            total_sum=total_sum+(product_obj.final_price)*quantity
        # print(cart[0].coupon)    
        # print(total_sum)
        total=total_sum
        #===
        
        if coupon:
            print('hi code')
        
            if int(total) >= coupon.minimum_amount :
                
                if cart[0].coupon == None and user_coupon_obj is None :
                    user_coupon.objects.create(coupon=coupon, user=user)
                    Cart.objects.filter(user=user).update(coupon=coupon)
                    messages.info(request, "Coupon applied successfully !")
                    
                    
                    print('hi2')
                    
                else:
                    messages.info(request, 'Coupon already applied ! ')    
                    print(f'hi ============ {coupon.user}')
                      
            else:
                messages.info(request, f'Aleast spent Rs {coupon.minimum_amount} ! ')
            
            
            
            return redirect('choose_payment_method', id)
        elif coupon_code == '':
            messages.error(request, 'Please enter a coupon code ! ')
            return redirect('choose_payment_method', id)
        else:
            messages.error(request, 'Not a valid coupon !')
            return redirect('choose_payment_method', id)
       
    else:
        return redirect('choose_payment_method', id) 

def wallet(request):
    if "user_id" in request.session: 
        user=User.objects.get(email=request.session['user_id'])
        try:
            wallet=Wallet.objects.get(user=user)
        except:
            wallet=None  
        wallet_transactions=WalletTransactions.objects.filter(user=user)
        return render(request,'authenticate/wallet.html',{'wallet':wallet,'wallet_transactions':wallet_transactions})
    else:
        return redirect('choose_payment_method', id)    


def return_order(request,id):
    if "user_id" in request.session: 
        pass
        
        order_products = OrderItem.objects.filter(order_id=id)
        order=OrderTable.objects.get(id=id)
        order.status = "Returned"
        order.save()
        
        try:
            Wallet.objects.get(user = User.objects.get(email=request.session['user_id'])  )
            wallet=Wallet.objects.get(user = User.objects.get(email=request.session['user_id'])  )
            
            wallet.Balance += order.amount
            wallet.save()
        except:
            wallet=Wallet.objects.create(user = User.objects.get(email=request.session['user_id']), Balance = order.amount  )   
        
        for item in order_products:
            product=Product.objects.get(id=item.product_id)
            quantity=item.quantity
            print(product,quantity )
            product.total_quantity=product.total_quantity+quantity
            product.save()
        WalletTransactions.objects.create(amount = order.amount ,user = User.objects.get(email=request.session['user_id'])  , status = 'CREDIT' )
        print(order.amount)
            
        print(order.amount)
       
        return redirect(delivered_orders)
        #return HttpResponse('ghghhghg')
    else:
            return redirect(userlogin)    


