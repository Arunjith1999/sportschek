from unicodedata import name
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from login.models import OrderTable
from .models import Product, Category
from login.models import CustomUser,Coupen
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator,EmptyPage
import datetime
from .filters import orderFilter
from django.http import HttpResponse,FileResponse
import csv
import xlwt
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# Create your views here.
def admin_page(request):
    return render(request, 'authenticate/admin.html')


def admin_login(request):
    if 'admin_id' in request.session:
        return redirect(admin_home)
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == '' and password == '':
            messages.error(request, 'Please enter Email and password !')
            return redirect(admin_login)

        elif email != 'admin123@gmail.com':
            messages.error(request, 'Only admin can Login!!!')
            return redirect(admin_login)

        elif CustomUser.objects.filter(email=email):
            admin = authenticate(request, username=email, password=password)
            if admin is not None:

                request.session['admin_id'] = email
                login(request, admin)
                return redirect(admin_home)
            else:
                messages.error(request, 'No such user')
                return redirect(admin_login)
        else:

            messages.error(request, 'Invalid credentials')
            return redirect(admin_login)
    return render(request, 'Admin/adminlogin.html')


def admin_home(request):
    if 'admin_id' in request.session:
        products = Product.objects.all()
        confirmed_orders = OrderTable.objects.filter(status = 'Confirmed').count()
        pending_orders = OrderTable.objects.filter(status = 'Pending').count()
        delivered_orders = OrderTable.objects.filter(status = 'Delivered').count()
        from datetime import timedelta
        from django.utils import timezone
        
        
        
        order_today = OrderTable.objects.filter(date_delivered = datetime. date. today(), status='Delivered' ).count()
        order_today_obj = OrderTable.objects.filter(date_delivered = datetime. date. today(), status='Delivered' )
        revenue_today=0
        for i in order_today_obj:
            revenue_today=i.amount+revenue_today
        some_day_last_week = datetime. date. today() -datetime.timedelta(days=7)
       
        order_lastweek=OrderTable.objects.filter(date_delivered__gte=some_day_last_week, date_delivered__lte=datetime. date. today(), status='Delivered').count()
        order_lastweek_obj=OrderTable.objects.filter(date_delivered__gte=some_day_last_week, date_delivered__lte=datetime. date. today(), status='Delivered')
        revenue_lastweek=0
        for i in order_lastweek_obj:
            revenue_lastweek=i.amount+revenue_lastweek
        
        some_day_last_year = datetime. date. today() -datetime.timedelta(days=365)
       
        order_lastyear=OrderTable.objects.filter(date_delivered__gte=some_day_last_year, date_delivered__lte=datetime. date. today(), status='Delivered').count()
        order_lastyear_obj=OrderTable.objects.filter(date_delivered__gte=some_day_last_year, date_delivered__lte=datetime. date. today(), status='Delivered')
        
        revenue_lastyear=0
        for i in order_lastyear_obj:
            revenue_lastyear=i.amount+revenue_lastyear
        
        yesterday = datetime. date. today() -datetime.timedelta(days=1)
        yesterday_1 = datetime. date. today() -datetime.timedelta(days=2)
        yesterday_2 = datetime. date. today() -datetime.timedelta(days=3)
        yesterday_3 = datetime. date. today() -datetime.timedelta(days=4)
        yesterday_4 = datetime. date. today() -datetime.timedelta(days=5)
        yesterday_5 = datetime. date. today() -datetime.timedelta(days=6)
        yesterday_6 = datetime. date. today() -datetime.timedelta(days=7)

        order_yesterday=OrderTable.objects.filter(date_delivered__gte=yesterday, date_delivered__lte=datetime. date.today(), status='Delivered').count()
        order_yesterday_1=OrderTable.objects.filter(date_delivered__gte=yesterday_1, date_delivered__lte=yesterday, status='Delivered').count()
        order_yesterday_2=OrderTable.objects.filter(date_delivered__gte=yesterday_2, date_delivered__lte=yesterday_1, status='Delivered').count()
        order_yesterday_3=OrderTable.objects.filter(date_delivered__gte=yesterday_3, date_delivered__lte=yesterday_2, status='Delivered').count()
        order_yesterday_4=OrderTable.objects.filter(date_delivered__gte=yesterday_4, date_delivered__lte=yesterday_3, status='Delivered').count()
        order_yesterday_5=OrderTable.objects.filter(date_delivered__gte=yesterday_5, date_delivered__lte=yesterday_4, status='Delivered').count()
        order_yesterday_6=OrderTable.objects.filter(date_delivered__gte=yesterday_6, date_delivered__lte=yesterday_5, status='Delivered').count()
    
        context={'revenue_today':revenue_today,
                 'revenue_lastweek':revenue_lastweek,
                 'revenue_lastyear':revenue_lastyear,
                 
                 'order_today':order_today,
                'yesterday':yesterday,
                'yesterday_1':yesterday_1,
                'yesterday_2':yesterday_2,
                'yesterday_3':yesterday_3,
                'yesterday_4':yesterday_4,
                'yesterday_5':yesterday_5,
                'yesterday_6':yesterday_6,
            
            
                'order_yesterday':order_yesterday,
                'order_yesterday_1':order_yesterday_1,
                'order_yesterday_2':order_yesterday_2,
                'order_yesterday_3':order_yesterday_3,
                'order_yesterday_4':order_yesterday_4,
                'order_yesterday_5':order_yesterday_5,
                'order_yesterday_6':order_yesterday_6,
                
                'confirmed_orders':confirmed_orders,
                'pending_orders':pending_orders,
                'delivered_orders':delivered_orders,
                
                'order_today':order_today,
                'order_lastweek':order_lastweek,
                'order_lastyear':order_lastyear,

                
                }
        
        
        return render(request, 'admin/admin_home.html', context)
    return redirect(admin_login)


def customers(request):
    customers = CustomUser.objects.filter(is_active=True, is_superuser=False).order_by('first_name').values()
    return render(request, 'Admin/customer.html', {'customers': customers})


# ===============================================================================================================================

#  Block    Unblock       

def block(request, id):
    CustomUser.objects.filter(id=id).update(is_active=False)
    messages.success(request, 'User Blocked successfully', )
    return redirect('customers')


def unblock(request, id):
    CustomUser.objects.filter(id=id).update(is_active=True)
    messages.success(request, 'User Unblocked successfully', )
    return redirect('blocked_customers')


def blocked_customers(request):
    customers = CustomUser.objects.filter(is_active=False, is_superuser=False).order_by('first_name').values()

    return render(request, 'Admin/blocked_customers.html', {'customers': customers})


# Product CRUD ========================================================================================================================


def Admin_products(request):
    if 'admin_id' in request.session:
        products = Product.objects.all().order_by('name').values()
        p=Paginator(products,7)
        page_num= request.GET.get('page',4)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page= p.page(1)

        cate = Category.objects.all()
        return render(request, 'Admin/product.html', {'product': page, 'cate': cate})
    else:
        return redirect(admin_login)


def add_product(request):
    if 'admin_id' in request.session:
        cat = None
        if request.method == 'POST':
            name = request.POST['name']
            description = request.POST['product_description']
            price = request.POST['price']
            total_quantity = request.POST['quantity']
            category = Category.objects.get(id=request.POST['category'])
            offer = request.POST['offer']
            image = image2 = image3 = ''
            try:
                image = request.FILES['uploadFromPC']
                image2 = request.FILES['uploadFromPC2']
                image3 = request.FILES['uploadFromPC3']
            except:
                print('please add an image')

            if name == '' or description == '' or price == '' or total_quantity == '' or image == '':
                messages.error(request, 'All fields are required')
            elif int(price) <0 :   
                 messages.error(request,'Negative number is not supportted for price and stock', extra_tags='productadderror')
                 return redirect(add_product)
            elif category == '':
                messages.error(request, 'Please select a category', extra_tags='productadderror')
                return redirect(add_product)
            elif offer == '' or int(offer)<0 or int(offer)>100:
                messages.error(request,'Offer must be between 1 and 100', extra_tags='productadderror')
                return redirect(add_product)    

            elif image == None or image2==None or image3 == None or (image == None and image2==None) or ((image == None and image3==None) or (image3 == None and image2==None) or ((image == None and image2==None and image3==None)))  :
                messages.error(request,'Please add product image', extra_tags='productadderror')
                return redirect(add_product)


            else:
                product = Product.objects.create(name=name, category=category, description=description, price=price,
                                                  total_quantity=total_quantity, image=image, image2=image2,offer=offer,
                                                  image3=image3)
                product.save()
                messages.success(request, 'Product added sucessfully', extra_tags='productadderror')
                return redirect(add_product)

        cat = Category.objects.all()
        return render(request, 'Admin/add_product.html', {'cat': cat,})
    else:
        return redirect(admin_login)


def delete_product(request, id):
        print('hi')
        products = Product.objects.get(id=id)
        products.delete()
        return redirect(Admin_products)
   


def update_product(request, id):
    if 'admin_id' in request.session:
        product = Product.objects.get(id=id)

        if request.method == 'POST':
            name = request.POST['name']
            description = request.POST['product_description']
            price = request.POST['price']
            total_quantity = int(request.POST['quantity'])
           # category = Category.objects.get(id=request.POST['category'])
            offer = request.POST['offer']
            #in_stock = request.POST['in_stock']
            # image = image2=image3=''
            # try:
            #     image = request.FILES['uploadFromPC']
            #     image2 = request.FILES['uploadFromPC2']
            #     image3  = request.FILES['uploadFromPC3']
            # except:
            #     print('please add an image')

            if(total_quantity > 0 ):
                instock= True
            else:
                instock = False
            category = Category.objects.get(id=request.POST['category'])            

            if name == '' or description == '' or price == '' or total_quantity == '' :
                messages.error(request, 'All fields are required')
            elif int(price)<0:
                messages.error(request,'Negative number is not supportted for price', extra_tags='productadderror')
                return redirect('update_product',id)
            elif offer == '' or int(offer)<0 or int(offer)>100:
                messages.error(request,'offer must be between 1 and 100',extra_tags='productadderror')
                return redirect('update_product',id)
            # elif image == None or image2==None or image3 == None or (image == None and image2==None) or ((image == None and image3==None) or (image3 == None and image2==None) or ((image == None and image2==None and image3==None)))  :
            #     messages.error(request,'Please add product image', extra_tags='productadderror')
            #     return redirect('update_product', id)    

            elif category == '':
                messages.error(request, 'Please select a category', extra_tags='productadderror')
                return redirect(update_product)

            else:

                product = Product.objects.filter(id=id).update(name=name, category=category, description=description,
                                                                price=price,
                                                                total_quantity=total_quantity,offer=offer,instock = instock )
            # product.save()     
        cat = Category.objects.all()
    
        return render(request, 'Admin/update_product.html', {'cat': cat, 'product': product}, )
    else:
        return redirect(admin_login)    


# category management ==================================================================================================================


def admin_category(request):
    if 'admin_id' in request.session:
        category = Category.objects.all()
        p=Paginator(category , 7)
        page_num= request.GET.get('page',4)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page=p.page(1)

        return render(request, 'Admin/category.html', {'category': page})

    else:
        return redirect(admin_login)


def delete_category(request, id):
    cat = Category.objects.get(id=id)
    cat.delete()
    return redirect(admin_category)


def add_category(request):
    if 'admin_id' in request.session:
        if request.method == 'POST':
            name = request.POST['name']
            description = request.POST['description']
            offer = request.POST['offer']
            if name == '' or description == '':
                messages.error(request, 'All fields are necessary')
                return redirect(add_category)
            else:
                category = Category.objects.create(name=name, description=description)
                category.save()
                messages.success(request, 'category added sucessfully')
                return redirect(admin_category)

        return render(request, 'Admin/add_category.html')
    else:
        return redirect(admin_login)


def edit_category(request, id):
    if 'admin_id' in request.session:
        category = Category.objects.get(id=id)
        if request.method == 'POST':
            name = request.POST['name']
            description = request.POST['description']
            offer = request.POST['offer']
            if name == '' or description == '':
                messages.error(request, 'All fields are necessary')
                return redirect('edit_category',id)
            elif offer=='' or int(offer)<0 or int(offer)>100:
                messages.error(request,'offer must be between 1 and 100',extra_tags='productadderror')
                return redirect('edit_category',id)   
            else:
                category = Category.objects.filter(id=id).update(name=name, description=description,offer=offer)
                messages.success(request, 'category Update successfully')
                return redirect(admin_category)
        return render(request, 'Admin/edit_category.html', {'data': category})
    else:
        return redirect(admin_login)


def admin_logout(request):
    request.session.flush()
    logout(request)
    return redirect(admin_login)


#=============ORDER MANAGEMENT==============
def orders(request):
    if 'admin_id' in request.session:
        order= OrderTable.objects.filter(Q(status='Pending')|Q(status="Rejected")).order_by('created_at').values()
        p = Paginator(order,7)
        page_num = request.GET.get('page',1)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        return render (request,'Admin/order.html',{'order':page,'page_number':p})



def accept_order(request,id) :      
  OrderTable.objects.filter(id=id).update(status='Confirmed')
  messages.success(request,'Order Confirmed Successfully')
  return redirect(orders)


def reject_order(request,id):
    OrderTable.objects.filter(id=id).update(status='Rejected')  
    messages.success(request,'Order Rejected')
    return redirect(orders)

def order_progress(request):
    if 'admin_id' in request.session:
        order=OrderTable.objects.filter(Q(status='Confirmed')).order_by('created_at').values()
        p = Paginator(order,7)
        page_num = request.GET.get('page',1)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        return render(request,'Admin/order_progress.html',{'order':page,'page_number':p})


def completed_orders(request):
    if 'admin_id' in request.session:
        order=OrderTable.objects.filter(Q(status='Delivered')).order_by('created_at').values() 
        p = Paginator(order,7)
        page_num = request.GET.get('page',1)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
            
        return render (request,'Admin/completed_order.html',{'order':page,'page_number':p})   



def delivery(request,id):
    if 'admin_id' in request.session:
        OrderTable.objects.filter(id=id).update(status='Delivered',date_delivered= datetime. date. today(),is_paid=True)   
        messages.success(request,'Product out for delivery')
        return redirect(completed_orders) 


# def Coupon(request):
#     if 'admin_id' in request.session:
#        if request.method =='POST': 
#           code=request.POST['code']
          
#           discount=request.POST['discount']
#           minimum_price=request.POST['minimum_price']
#           print(code, discount, minimum_price)
#           if code == "" or discount =="" or minimum_price =="":
#              print('hi if ')
#              messages.error(request,'all fields are neccessary')
#              return redirect(Coupon)
#           else:
#             print('hi else ')
#             coupn=coupon.objects.create(code=code,discount=discount,minimum_price=minimum_price)
#             coupn.save()
              
#             messages.success(request,'Coupon created successfully')
       
#        return render(request,'Admin/coupon.html')   
#     return redirect(admin_login)      

def all_report(request):
    if 'admin_id' in request.session:
        order = OrderTable.objects.filter(status='Delivered').order_by('id')
        p = Paginator(order , 10)
        page_num = request.GET.get('page',1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)    

       
        revenue=0
        for i in order:
            revenue=i.amount+revenue
        return render(request,'admin/sales_report.html',{'order':page,'revenue':revenue,'page_number':p})
    else:
        return redirect(admin_login)    



def sales_report_custom(request):
    if'admin_id' in request.session:
        startdate = request.GET['startdate']
        enddate = request.GET['enddate']
        if startdate == '' or enddate == '' or(startdate =='' and enddate ==''):
            messages.error(request,'enter valid dates')
            return redirect(all_report)
        order_today = OrderTable.objects.filter(date_delivered__gte=startdate, date_delivered__lte=enddate, status='Delivered').order_by('id')
        revenue = 0
        p=Paginator(order_today,10)
        page_num = request.GET.get('page',1)
        try:
            page=p.page(page_num)
        except EmptyPage:
            page=p.page(1)

        for i in order_today:
            revenue = i.amount+revenue
        return render(request,'admin/sales_report_custom.html',{'order_today':page,'revenue':revenue,'startdate':startdate,'enddate':enddate,'page_number':p})
    else:
        return redirect(admin_login)            


@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def sales_report_daily(request):
    
    if 'admin_id' in request.session:
        
        order_today = OrderTable.objects.filter(date_delivered = datetime. date. today(), status='Delivered' ).order_by('id')
        revenue=0
        
        p=Paginator(order_today, 7)
        page_num = request.GET.get('page',1)
        
        # print("NUMBER OF PAGES")
        # print(p.num_pages)
        try:
            
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        #print(page) 
        
        
        print(order_today)
        for i in order_today:
            revenue=i.amount+revenue
            
        return render(request, 'admin/sales_report_daily.html', {'order_today':page, 'revenue':revenue,'page_number':p} )    
    else:
        return redirect(admin_login)  



@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def sales_report_weekly(request):
    
    if 'admin_id' in request.session:
        from datetime import timedelta
        from django.utils import timezone
        some_day_last_week = datetime. date. today() -datetime.timedelta(days=7)
       
        order_today=OrderTable.objects.filter(date_delivered__gte=some_day_last_week, date_delivered__lte=datetime. date. today(), status='Delivered').order_by('id')
        
        #order_today=orderFilter.qs
        
        p=Paginator(order_today, 7)
        page_num = request.GET.get('page',1)
        
        # print("NUMBER OF PAGES")
        # print(p.num_pages)
        try:
            
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        #print(page) 
        
        
        print(some_day_last_week)
        #OrderTable.objects.filter(date_delivered = datetime. date. today() )
        revenue=0
        #print(order_today)
        for i in order_today:
            revenue=i.amount+revenue
            
        return render(request, 'admin/sales_report_weekly.html', {'order_today':page, 'revenue':revenue,'page_number':p} )    
    else:
        return redirect(admin_login)  


@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def sales_report_yearly(request):
    
    if 'admin_id' in request.session:
        from datetime import timedelta
        from django.utils import timezone
        some_day_last_week = datetime. date. today() -datetime.timedelta(days=365)
       
        order_today=OrderTable.objects.filter(date_delivered__gte=some_day_last_week, date_delivered__lte=datetime. date. today(), status='Delivered').order_by('id')
        
        p=Paginator(order_today, 15)
        page_num = request.GET.get('page',1)
        
        # print("NUMBER OF PAGES")
        # print(p.num_pages)
        try:
            
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        #print(page) 
        print(some_day_last_week)
        #OrderTable.objects.filter(date_delivered = datetime. date. today() )
        revenue=0
        #print(order_today)
        for i in order_today:
            revenue=i.amount+revenue
            
        return render(request, 'admin/sales_report_yearly.html', {'order_today':page, 'revenue':revenue,'page_number':p} )    
    else:
        return redirect(admin_login)  



def export_csv(request):
    
    # response = HttpResponse(content_type="text/csv")
    # response['Content-Dsiposition'] = 'attachment; filename=Expenses' + \
    #     datetime.datetime.now()+'.csv'
    
    # writer=csv.writer{response}
    
    # writer.writerow     
    pass

    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)         
        
def edit_prduct_offer(request, id):
    products = Product.objects.all()
    product = Product.objects.get(id=id) 
    print( id)
    return render(request, 'admin/edit_prduct_offer.html', {'product':product, 'products':products})    


#=========================================
#==========Coupon==========================
from superuser.models import Coupen
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def coupons(request):
    if 'admin_id' in request.session:
        coupon = Coupen.objects.all()
        print(coupon)
        return render(request, "admin/coupons.html", {'coupon':coupon})
    else:
        return redirect(admin_login)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def add_coupon(request):
    
    import string
    import random
    N = 9
    res = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=N))
    if 'admin_id' in request.session:
        if request.method == 'POST':
            code = request.POST['code']
            minimum = request.POST['minimum']
            discount = request.POST['discount']
            # initializing size of string
            
            
            # using random.choices()
            # generating random strings
            res = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=N))
            
            while Coupen.objects.filter(coupon_code=str(res)) is None:
                    res = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=N))
                    #tracking_no=tracking_no
            print(res)
            # print result
            print("The generated random string : " + str(res))
            
            Coupen.objects.create(coupon_code=code, minimum_amount=minimum, discount_price=discount)
        return render(request, "admin/add_coupon.html",{'code':str(res)} )
    else:
        return redirect(admin_login)    


#===============Offers================
def offers(request):
    if'admin_id' in request.session:
        products=Product.objects.exclude(offer = 0)
        return render(request,'admin/offers.html',{'products':products})
    return redirect(admin_login)    


# def add_Product_offer(request):
#     if 'admin_id' in request.session:
#         if request.method == 'POST':
#             offer=request.POST['offer']
#             name=Product.objects.get(id=request.POST['name'])
#             if offer=='' or int(offer)<0 or int(offer)>100:
#                 messages.error(request,'offer must be between 0 and 100')
#                 return redirect(Product_offer)
#             ofer=product_offer.objects.create(offer=offer,name=name)
#             ofer.save()
#             messages.success(request,'offer addded sucessfully')
#         prod=Product.objects.all()
#         return render(request,'admin/add_product_offer.html',{'prod':prod})    

#     else:
#         return redirect(admin_login)    


def add_new_product_offer(request):
    
    products = Product.objects.filter(offer = 0)
    if request.method == 'POST':
        
            offer = request.POST['offer']
            id = request.POST['product']
            
            
            if offer == '' or int(offer)<0 or int(offer)>100:
                messages.error(request,'Offer must be between 1 and 100', extra_tags='productadderror')
            elif id == '':
                messages.error(request,'select a product', extra_tags='productadderror')
            else:
                    
                Product.objects.filter(id=id).update(offer=offer)
            
                messages.success(request,'Offer added sucessfully', extra_tags='productadderror')
                return redirect(offers)
    
    return render(request, 'admin/add_product_offer.html', { 'products':products})    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)         
        
def delete_product_offer(request, id):
    product = Product.objects.filter(id=id).update(offer=0)
    
    return redirect(offers)  


@cache_control(no_cache=True, must_revalidate=True, no_store=True)         
        
def delete_category_offer(request, id):
    product = Category.objects.filter(id=id).update(offer=0)
    
    return redirect(category_offers)  


      
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)         
        
def edit_product_offer(request, id):
    products = Product.objects.get(id=id)
    cat=Product.objects.all()
    if request.method =='POST':
        offer = request.POST['offer']
        if offer =="" or int(offer)<0 or int(offer) >=100:
            messages.error(request,'invalid offer')
            return redirect('edit_product_offer',id)
        products=Product.objects.filter(id=id).update(offer=offer)
        messages.success(request,"offer updated successfully")
        return redirect(offers)
        
    return render(request, 'admin/edit_product_offer.html', { 'products':products,'cat':cat})    

def edit_category_offer(request, id):
    cat = Category.objects.all()
    product = Category.objects.get(id=id) 
    if request.method == 'POST':
        offer = request.POST['offer']
        if offer =="" or int(offer)<0 or int(offer)>=100:
            messages.error(request,'enter valid offers')
            return redirect('edit_category_offer',id)
        product = Category.objects.filter(id=id).update(offer=offer) 
        messages.success(request,'offer updated successfully')
        return redirect(offers)   

    print( id)
    return render(request, 'admin/edit_category_offer.html', {'product':product, 'cat':cat})    



@cache_control(no_cache=True, must_revalidate=True, no_store=True)         
        
def category_offers(request):
    cat = Category.objects.exclude(offer = 0)
    
    print( id)
    return render(request, 'admin/category_offers.html', { 'products':cat})    

      

@cache_control(no_cache=True, must_revalidate=True, no_store=True)         
        
def add_new_category_offer(request):
    cat = Category.objects.filter(offer = 0)
    
    if request.method == 'POST':
        
            offer = request.POST['offer']
            id = request.POST['product']
            
            
            if offer == '' or int(offer)<0 or int(offer)>100:
                messages.error(request,'Offer must be between 1 and 100', extra_tags='productadderror')
            elif id == '':
                messages.error(request,'select a category', extra_tags='productadderror')
            else:
                    
                Category.objects.filter(id=id).update(offer=offer)
            
                messages.success(request,'Offer added sucessfully', extra_tags='productadderror')
                return redirect(category_offers)
    
    
    
    return render(request, 'admin/add_new_category_offer.html', { 'cat':cat})    


def export_csv_yearly(request):
    if 'admin_id' in request.session:
        some_day_last_week = datetime.date.today() -datetime.timedelta(days=365)
        orders = OrderTable.objects.filter(date_delivered__gte=some_day_last_week, date_delivered__ite=datetime.date.today(),status='Delivered').order_by('id')
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment: filename=Orders' + \
           str(datetime.datetime.now())+'.csv'

        writer=csv.writer(response)
        writer.writerow(['order Id','Amount','Name','Phone number','Payment_method','ordered_date','Delivered Date'])

        for order in orders:
            writer.writerow([order.id,order.amount,order.name,order.phone_number,order.payment_method,order.created_at,order.date_delivered])
        return response
    else:
        return redirect(admin_login)

def export_csv_weekly(request):
    if 'admin_id' in request.session:
        some_day_last_week = datetime.date.today() -datetime.timedelta(days=7)
        orders=OrderTable.objects.filter(date_delivered__gte=some_day_last_week,date_delivered__lte=datetime.date.today(),status='Delivered').order_by('id')
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment: filename=orders' + \
            str(datetime.datetime.now())+'.csv'
        writer = csv.writer(response)
        writer.writerow(['order Id','Amount','Name','Phone number','Payment_method','ordered_date','Delivered Date'])    
        for order in orders:
            writer.writerow([order.id,order.amount,order.name,order.phone_number,order.payment_method,order.created_at,order.date_delivered])
        return response
    else:
        return redirect(admin_login)      

def export_csv_daily(request):
    if 'admin_id' in request.session:
        
        orders = OrderTable.objects.filter(date_delivered = datetime. date. today(), status='Delivered' ).order_by('id')
            
        
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=Orders' + \
            str(datetime.datetime.now())+'.csv'
        
        writer=csv.writer(response)
        
        writer.writerow(['Order Id','Amount', 'Name','Phone number', "Payment method" 'Ordered date',  'Delivereed Date'])
        
        
        for order in orders:
            writer.writerow([order.id ,order.amount, order.name, order.phone_number,order.payment_method, order.created_at, order.date_delivered])
        
        return response
    else:
        return redirect(admin_login)  
    
    
def export_csv_custom(request):
    if 'admin_id' in request.session:
        
        startdate = request.GET['startdate']
        
        enddate   = request.GET['enddate']
        
        orders = OrderTable.objects.filter(date_delivered__gte= startdate,date_delivered__lte = enddate, status='Delivered' ).order_by('id')  
            
        
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=Orders' + \
            str(datetime.datetime.now())+'.csv'
        
        writer=csv.writer(response)
        
        writer.writerow(['Order Id','Amount', 'Name','Phone number', "Payment method" 'Ordered date',  'Delivereed Date'])
        
        
        for order in orders:
            writer.writerow([order.id ,order.amount, order.name, order.phone_number,order.payment_method, order.created_at, order.date_delivered])
        
        return response
    else:
        return redirect(admin_login)   


def export_excel_yearly(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Orders' + \
            str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Sales')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold =True   
    
    columns = ['Order Id','Amount', 'Name','Phone number', "Payment method" 'Ordered date',  'Delivereed Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style=xlwt.XFStyle() 
    
    some_day_last_week = datetime. date. today() -datetime.timedelta(days=365)
        
    rows=OrderTable.objects.filter(date_delivered__gte=some_day_last_week, date_delivered__lte=datetime. date. today(), status='Delivered').values_list('id','amount', 'name','phone_number', 'payment_method', 'created_at',  'date_delivered')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]),font_style)
    wb.save(response)
    return  response

def export_excel_daily(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Orders' + \
            str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Sales')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold =True   
    
    columns = ['Order Id','Amount', 'Name','Phone number', "Payment method" 'Ordered date',  'Delivereed Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style=xlwt.XFStyle() 
    
    
        
    rows=OrderTable.objects.filter(date_delivered = datetime. date. today(), status='Delivered' ).values_list('id','amount', 'name','phone_number', 'payment_method', 'created_at',  'date_delivered')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]),font_style)
    wb.save(response)
    return  response

def export_excel_weekly(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Orders' + \
            str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Sales')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold =True   
    
    columns = ['Order Id','Amount', 'Name','Phone number', "Payment method" 'Ordered date',  'Delivereed Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style=xlwt.XFStyle() 
    
    some_day_last_week = datetime. date. today() -datetime.timedelta(days=7)
        
    rows=OrderTable.objects.filter(date_delivered__gte=some_day_last_week, date_delivered__lte=datetime. date. today(), status='Delivered').values_list('id','amount', 'name','phone_number', 'payment_method', 'created_at',  'date_delivered')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]),font_style)
    wb.save(response)
    return  response

def export_excel_custom(request):
    startdate = request.GET['startdate']
        
    enddate   = request.GET['enddate']
        
    
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Orders' + \
            str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Sales')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold =True   
    
    columns = ['Order Id','Amount', 'Name','Phone number', "Payment method" 'Ordered date',  'Delivereed Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style=xlwt.XFStyle() 
    
    some_day_last_week = datetime. date. today() -datetime.timedelta(days=7)
        
    rows=OrderTable.objects.filter(date_delivered__gte= startdate,date_delivered__lte = enddate, status='Delivered' ).values_list('id','amount', 'name','phone_number', 'payment_method', 'created_at',  'date_delivered')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]),font_style)
    wb.save(response)
    return  response
def export_pdf_yearly(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Sales' + \
        str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    html_string=render_to_string('admin/sales_pdf_yearly',{'sales':{},'total':0})
    html = HTML(string=html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output=open(output.name,'rb')
        response.write(output.read())
    return response
def export_pdf_old(request):
    if 'admin_id' in request.session:
        # create bytestream buffer
        buf = io.BytesIO()
        # Create a canvas 
        c = canvas.Canvas(buf,pagesize=letter, bottomup=0)
        # Create a text object 
        textobj = c.beginText()
        
        textobj.setTextOrigin(inch,inch)
        textobj.setFont('Helvetica',14)
        
        lines = [
            'mj','kl','kl'
        ]
        for line in lines:
            textobj.textLine(line)
        
        c.drawText(textobj)
        c.showPage()
        c.save()    
        buf.seek(0)
        return FileResponse(buf, as_attachment=True, filename="sales.pdf")
    else:
        return redirect(admin_login)                   


