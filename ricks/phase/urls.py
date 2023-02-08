from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('shop/', views.shop, name='shop'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('usersignup/', views.usersignup, name='usersignup'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('adminuserlist/', views.adminuserlist, name='adminuserlist'),
    path('adminproductlist/', views.adminproductlist, name='adminproductlist'),
    path('adminaddproduct/', views.adminaddproduct, name='adminaddproduct'),
    path('updateproduct/', views.updateproduct, name='updateproduct'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('userblock/', views.userblock, name='userblock'),
    path('userdelete/', views.userdelete, name='userdelete'),
    path('deleteproduct/', views.deleteproduct, name='deleteproduct'),
    path('adminaddcategory/', views.adminaddcategory, name='adminaddcategory'),
    path('shopsingle/', views.shopsingle, name='shopsingle'),
    path('updateproduct/<int:id>', views.updateproduct, name='updateproduct'),
    path('admincategorylist/', views.admincategorylist, name='admincategorylist'),
    path('deletecategory/', views.deletecategory, name='deletecategory'),
    path('updatecategory/', views.updatecategory, name='updatecategory'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('cart/', views.cart, name='cart'),
    path('otp/', views.otp, name='otp'),
    path('checkout/', views.checkout, name='checkout'),

]