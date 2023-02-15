from django.shortcuts import render, redirect
from phase.forms.user import UserSignupForm, UserLoginForm, UserAddressForm, OrderForm
from phase.forms.product import ProductForm
from phase.forms.category import CategoryForm
from .models import UserDetail, Product, Category, Cart, CartItem, Address, Order
from django.contrib.auth.models import User
import requests, random
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, F
from django.core.paginator import Paginator

def index(request):
    return render(request, 'index.html')

def userlogin(request):
    if 'uname' in request.session:
        return redirect('shop')
    else:        
        if request.method=='POST':
            uname = request.POST.get('uname')
            password = request.POST.get('upassword')
            customer = UserDetail.objects.filter(uname=uname).first()
            if customer.upassword==password:
                if customer.uactive:
                    #request.session['uname']=uname
                    request.session['some_data'] = uname
                    return redirect('otp')
            else:
                return redirect('userlogin')
        fm = UserLoginForm()
        return render(request, 'userlogin.html',{'fm':fm})


def usersignup(request):
    if request.method=='POST':
        fm = UserSignupForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('userlogin') 
        else:
            return redirect('usersignup')
    fm = UserSignupForm()
    return render (request, 'usersignup.html',{'fm':fm})



def shop(request):
    if 'uname' in request.session:
        details3=Product.objects.all()
        return render(request, 'shop.html', {'mymembers3': details3})
    else:
         return redirect('userlogin')

def shopsingle(request):
    if 'uname' in request.session:
        uid=request.GET['uid']
        details4=Product.objects.filter(id=uid).first()
        return render(request, 'shopsingle.html', {'mymembers4': details4})
    else:
        return render(request, 'userlogin.html')

def adminlogin(request):
    if 'username' in request.session:
        return redirect('admindashboard')
    else:    
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                request.session['username']=username
                return redirect('admindashboard')           
            else:
                return render (request, 'adminlogin.html')

        return render(request, 'adminlogin.html')

def admindashboard(request):
    if 'username' in request.session:
        return render(request, 'admindashboard.html')
    else:
        return render(request, 'adminlogin.html')
    
def adminlogout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('adminlogin')

def adminuserlist(request):
    if 'username' in request.session:
        if 'search' in request.GET:
            search=request.GET['search']
            details=UserDetail.objects.filter(uname__icontains=search)
        else:
            details=UserDetail.objects.all().order_by('-id')
        return render(request,'adminuserlist.html',{'mymembers': details})
    else:
        return render(request, 'adminlogin.html')

def adminproductlist(request):
    if 'username' in request.session:
        if 'search' in request.GET:
            search=request.GET['search']
            details2=Product.objects.filter(name__icontains=search)
        else:
            details2=Product.objects.all().order_by('-id')
        return render(request,'adminproductlist.html',{'mymembers2': details2})
    else:
        return render(request, 'adminlogin.html')
    
def adminaddproduct(request):
    if 'username' in request.session:       
        if request.method == 'POST':
            fm = ProductForm(request.POST,request.FILES)
            if fm.is_valid():
                fm.save()
                return redirect('adminproductlist')
        
        else:        
            fm = ProductForm()
            return render(request, 'adminaddproduct.html',{'fm':fm})
    else:
        return render(request, 'adminlogin.html')
    
def adminaddcategory(request):
    if 'username' in request.session:       
        if request.method == 'POST':
            fm = CategoryForm(request.POST,request.FILES)
            if fm.is_valid():
                name = fm.cleaned_data['name']
                dup = Category.objects.filter(name=name).first()
                if dup:
                    messages.warning(request,'Category already exists')
                    return redirect('adminaddcategory')
                else: 
                    fm.save()
                    return redirect('admincategorylist')       
        else:        
            fm = CategoryForm()
            return render(request, 'adminaddcategory.html',{'fm':fm})
    else:
        return render(request, 'adminlogin.html')

def updateproduct(request,id):
    prod = Product.objects.get(id=id)
    if request.method == 'POST':
        fm = ProductForm(request.POST, request.FILES, instance=prod)
        if fm.is_valid():
            fm.save()
            return redirect('adminproductlist')
    else:
        fm = ProductForm(instance=prod)
        return render(request, 'adminupdateproduct.html', {'fm': fm})


    
def userblock(request):
    uid=request.GET['uid']
    block_check=UserDetail.objects.filter(id=uid)
    for x in block_check:
        if x.uactive:
            UserDetail.objects.filter(id=uid).update(uactive=False)
            messages.warning(request, f'{x.uname} is blocked')
        else:
            UserDetail.objects.filter(id=uid).update(uactive=True)
            messages.success(request, f'{x.uname} is unblocked')
    return redirect('adminuserlist')


def userlogout(request):
    if 'uname' in request.session:
        del request.session['uname']
        del request.session['some_data']
    return redirect('userlogin')

def userdelete(request):
    uid=request.GET['uid']
    UserDetail.objects.filter(id=uid).delete()
    return redirect('adminuserlist')

def deleteproduct(request):
    uid=request.GET['uid']
    Product.objects.filter(id=uid).delete()
    return redirect('adminproductlist')

def admincategorylist(request):
    if 'username' in request.session:
        if 'search' in request.GET:
            search=request.GET['search']
            details2=Category.objects.filter(name__icontains=search)
        else:
            details2=Category.objects.all().order_by('-id')
        return render(request,'admincategorylist.html',{'mymembers2': details2})
    else:
        return render(request, 'adminlogin.html')
    
def deletecategory(request):
    uid=request.GET['uid']
    Category.objects.filter(id=uid).delete()
    return redirect('admincategorylist')

def updatecategory(request):
    uid = request.GET['uid']
    cat = Category.objects.get(id=uid)
    print("!!!Inside!!")
    if request.method == 'POST':
        fm = CategoryForm(request.POST, request.FILES, instance=cat)
        if fm.is_valid():
            fm.save()
            return redirect('admincategorylist')
    else:
        fm = CategoryForm(instance=cat)
        return render(request, 'adminupdatecategory.html', {'fm': fm})
    


def otp(request):
    global otp_sent
    if request.method=='POST':
        otp_rec = int(request.POST.get('c_otp'))
        if otp_rec==otp_sent:
            request.session['uname'] = request.session['some_data']
            messages.success(request,"Login Completed Successfully")
            return redirect('shop')
        else:
            messages.warning(request, 'Incorrect OTP')
            return redirect('otp')
    else:

        otp_sent = random.randint(1001, 9999)
        use = request.session['some_data']
        obj = UserDetail.objects.get(uname=use)
        url = 'https://www.fast2sms.com/dev/bulkV2'
        payload = f'sender_id=TXTIND&message={otp_sent}&route=v3&language=english&numbers={obj.uphone}'
        headers = {
            'authorization': "xoiObB7WLa4GvY0uPZ6J9KmS1kXQCA2MeRhpzfTHN5sy8dctVDo5mkyeX9CRJxBKzu8M7FZ0stfh2gdi",
            'Content-Type': "application/x-www-form-urlencoded"
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text) 
        print("Sent value::",otp_sent)
    return render(request, 'otp.html')

def checkout(request):
    if request.method=='POST':
        fm = UserAddressForm(request.POST) 
        if fm.is_valid():
            use = request.session['uname']
            user = UserDetail.objects.get(uname = use)
            reg = fm.save(commit=False)
            reg.user = user
            reg.save()
            messages.success(request, 'new address added successfully')
            return redirect('checkout') 
        else:
            messages.warning(request,'Enter the address') 
            return redirect('checkout') 
    else:
        fm = UserAddressForm()
        use = request.session['uname']
        context=Address.objects.filter(user__uname = use).order_by('-id')
        ret = itemcalculate(use)
        return render(request, 'checkout.html', {'fm': fm, 'context': context, 'data':ret['data'], 'datap':ret['datap']})

def updateaddress(request,id):
    add = Address.objects.get(id=id)
    if request.method == 'POST':
        fm = UserAddressForm(request.POST, instance=add)
        if fm.is_valid():
            fm.save()
            messages.success(request,"Address updated successfully")
            return redirect('checkout')
    else:
        fm = UserAddressForm(instance=add)
        use = request.session['uname']
        context=Address.objects.filter(user__uname = use)
        ret = itemcalculate(use)
        return render(request, 'updateaddress.html', {'fm': fm, 'context': context, 'data':ret['data'], 'datap':ret['datap']})

def deleteaddress(request):
    uid=request.GET['uid']
    Address.objects.filter(id=uid).delete()
    return redirect('checkout')

def address_select(request):
    uid=request.GET['uid']
    select_check=Address.objects.filter(id=uid)
    for x in select_check:
        if x.selected:
            Address.objects.filter(id=uid).update(selected=False)
            messages.warning(request, f'{x.name} is Unselected')
        else:
            Address.objects.all().update(selected=False)
            Address.objects.filter(id=uid).update(selected=True)
            messages.success(request, f'{x.name} is Selected')
    return redirect('checkout')

def addtocart(request):
    use=request.session['uname']
    user=UserDetail.objects.get(uname=use)
    try:
        cart=Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart=Cart.objects.create(user=user)
    pid=request.POST['pid']
    try:
        product=Product.objects.get(id=pid)
    except Product.DoesNotExist:
        return redirect('shop')
    try:
        if product.stock < 1:
            messages.warning(request, 'Out of stock')
            return redirect('shop')
        else:
            cartitem=CartItem.objects.get(cart=cart,product=product)
            cartitem.quantity+=1
            product.stock-=1
            Product.objects.filter(id=pid).update(stock=product.stock)
    except CartItem.DoesNotExist:
        if product.stock < 1:
            messages.warning(request, 'Out of stock')
            return redirect('shop')
        else:
            cartitem=CartItem.objects.create(cart=cart,product=product,quantity=1)
            product.stock-=1
            Product.objects.filter(id=pid).update(stock=product.stock)

    cartitem.save()
    return redirect('cart')

def itemcalculate(name):
    total=0
    quantity=0
    set1=UserDetail.objects.filter(uname=name).first()
    set2=set1.id
    data=CartItem.objects.filter(cart__user__id=set2)
    for d in data:
        x=int(d.product.price)
        y=int(d.quantity)
        total += (x*y)
        quantity += d.quantity
    datap={
        "total":total,
        "quantity":quantity
    }
    return({'data':data, 'datap':datap})

def cart(request):
    name=request.session['uname']
    ret = itemcalculate(name)
    return render(request,'cart.html',ret)

def delcartitems(request):
    id=request.GET['id']
    it=CartItem.objects.get(cartitemid=id)
    cart_quantity = it.quantity
    cart_product = it.product.name
    Product.objects.filter(name=cart_product).update(stock=F('stock')+cart_quantity)
    CartItem.objects.filter(cartitemid=id).delete()
    return redirect('cart')

def payment(request):

    return render(request,'payment.html')



def order(request):
    user = request.session['uname']
    user = UserDetail.objects.get(uname = user)
    ord = Order.objects.filter(user=user).order_by('-id')
    return render(request,'order.html',{'ord':ord})

def thankyou(request):
    user = request.session['uname']
    use1 = UserDetail.objects.get(uname = user)
    use2 = Address.objects.get(user=use1,selected=True)
    cart = CartItem.objects.filter(cart__user__uname=use1)
    for c in cart:
        Order(user=use1, address=use2, product=c.product).save()
        c.delete() 
    return render(request,'thankyou.html')

def plus_cart(request):
    if request.method == 'GET':
        use = request.session['uname']
        user = UserDetail.objects.get(uname = use)
        prod_id=request.GET['prod_id']
        c = CartItem.objects.get(Q(product=prod_id) & Q(cart__user=user))
        c.quantity+=1
        c.save()
        Product.objects.filter(id=prod_id).update(stock=F('stock') - 1)
        d = CartItem.objects.get(Q(product=prod_id) & Q(cart__user=user))
        sub = d.subtotal
        ret = itemcalculate(use)
        datap = {
            'total': ret['datap']['total'],
            'quantity': ret['datap']['quantity'],
            'ind_subtotal': sub,
        }
        return JsonResponse(datap)
    
def minus_cart(request):
    print("Inside minus cart", request)
    if request.method == 'GET':
        use = request.session['uname']
        user = UserDetail.objects.get(uname = use)
        prod_id=request.GET['prod_id']
        c = CartItem.objects.get(Q(product=prod_id) & Q(cart__user=user))
        c.quantity-=1
        c.save()
        Product.objects.filter(id=prod_id).update(stock=F('stock') + 1)
        d = CartItem.objects.get(Q(product=prod_id) & Q(cart__user=user))
        sub = d.subtotal
        ret = itemcalculate(use)
        datap = {
            'total': ret['datap']['total'],
            'quantity': ret['datap']['quantity'],
            'ind_subtotal': sub,
        }
        return JsonResponse(datap)
    
def cancelorder(request,id):
    Order.objects.filter(id=id).update(status='Canceled')
    return redirect('order')

def returnorder(request,id):
    Order.objects.filter(id=id).update(status='Return')
    return redirect('order')


def adminorderlist(request):
    if 'search' in request.GET:
        search=request.GET['search']
        member=Order.objects.filter(user__uname__icontains=search).order_by('-id')
        paginator = Paginator(member, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        member = Order.objects.all().order_by('-id')
        paginator = Paginator(member, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request,'adminorderlist.html', {'page_obj': page_obj})

def updateorder(request,id):
    ord = Order.objects.get(id=id)
    if request.method == 'POST':
        fm = OrderForm(request.POST, request.FILES, instance=ord)
        if fm.is_valid():
            fm.save()
            return redirect('adminorderlist')
    else:
        fm = OrderForm(instance=ord)
        return render(request, 'adminupdateorder.html', {'fm': fm})
