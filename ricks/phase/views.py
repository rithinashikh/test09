from django.shortcuts import render, redirect
from phase.forms.user import UserSignupForm, UserLoginForm
from phase.forms.product import ProductForm
from phase.forms.category import CategoryForm
from .models import UserDetail, Product, Category, Cart, CartItem
from django.contrib.auth.models import User
import requests, random
from django.contrib import messages

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
                    request.session['uname']=uname
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

def userlogout(request):
    return redirect('userlogin')

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
            details=UserDetail.objects.all()
        return render(request,'adminuserlist.html',{'mymembers': details})
    else:
        return render(request, 'adminlogin.html')

def adminproductlist(request):
    if 'username' in request.session:
        if 'search' in request.GET:
            search=request.GET['search']
            details=Product.objects.filter(name__icontains=search)
        else:
            details2=Product.objects.all()
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
        else:
            UserDetail.objects.filter(id=uid).update(uactive=True)
    return redirect('adminuserlist')


def userlogout(request):
    if 'uname' in request.session:
        del request.session['uname']
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
            details=Category.objects.filter(name__icontains=search)
        else:
            details2=Category.objects.all()
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
    global r1
    if request.method=='POST':
        otp_ent = int(request.POST.get('c_otp'))
        if otp_ent==r1:
            return redirect('shop')
        else:
            print("!!! Incorrect OTP !!!")
            return redirect('otp')
    else:

        r1 = random.randint(1001, 9999)
        # url = 'https://www.fast2sms.com/dev/bulkV2'
        # message = r1
        # numbers = '9656791614'
        # payload = f'sender_id=TXTIND&message={message}&route=v3&language=english&numbers={numbers}'
        # headers = {
        #     'authorization': "xoiObB7WLa4GvY0uPZ6J9KmS1kXQCA2MeRhpzfTHN5sy8dctVDo5mkyeX9CRJxBKzu8M7FZ0stfh2gdi",
        #     'Content-Type': "application/x-www-form-urlencoded"
        #     }
        # response = requests.request("POST", url, data=payload, headers=headers)
        # print(response.text) 
        print("R1 Sent value::",r1)
    return render(request, 'otp.html')

def checkout(request):
    return render(request, 'checkout.html')

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
        cartitem=CartItem.objects.get(cart=cart,product=product)
        cartitem.quantity+=1
    except CartItem.DoesNotExist:
        cartitem=CartItem.objects.create(cart=cart,product=product,quantity=1)
    cartitem.save()
    return redirect('cart')

def cart(request):
    total=0
    quantity=0
    name=request.session['uname']
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
    return render(request,'cart.html',{'data':data, 'datap':datap})