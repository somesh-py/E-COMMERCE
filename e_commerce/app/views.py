from itertools import product
from statistics import quantiles
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Product, Customer, Cart, OrderPlaced
# from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .forms import *


# def home(request):
#  return render(request, 'app/home.html')

# class ProductView(View):
#     def get(self,request):
#         topwears=product.objects.filter(category='TW')
#         bottomwears=product.objects.filter(category='BW')
#         mobiles=product.objects.filter(category='M')
#         laptops=product.object.filter(category='L')
#         return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops})


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwear = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwear': bottomwear, 'mobiles': mobiles, 'laptops': laptops})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
            return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})
        else:
            return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})


# def add_to_cart(request):
#  return render(request, 'app/addtocart.html')

# def add_to_cart(request):
#     user=request.user
#     product_id=request.GET.get('prod_id')
#     product=Product.objects.get(id=product_id)
#     Cart(user=user,product=product).save()
#     return redirect('/cart')

def show_cart_data(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount += tempamount
                total_amount = amount+shipping_amount
            return render(request, 'app/addtocart.html', {'cart': cart, 'total_amount': total_amount, 'amount': amount})
        else:
            return render(request, 'app/empty.html')


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'Congratulation!! Profile Updated Succesfully')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


# def address(request):
#     return render(request, 'app/address.html')


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


def orders(request):
    return render(request, 'app/orders.html')


def change_password(request):
    return render(request, 'app/changepassword.html')


def mobile(request, data=None):
    if data == None:
        mobile = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Redmi' or data == 'Samsung' or data == 'Nokia' or data == 'Vivo' or data == 'Tecno' or data == 'Oppo' or data == 'iPhone' or data == 'realme' or data == 'iQOO' or data == 'OnePlus':
        mobile = Product.objects.filter(category='M').filter(brand=data)

    elif data == 'below':
        mobile = Product.objects.filter(
            category='M').filter(discounted_price__lt=10000)

    elif data == 'above':
        mobile = Product.objects.filter(
            category='M').filter(discounted_price__gt=10000)

    return render(request, 'app/mobile.html', {'mobiles': mobile})


# def laptop(request, data=None):
#     if data == None:
#         laptops = Product.objects.filter(category='L')
#     elif data == 'Lenovo' or data == 'HP' or data == 'Dell' or data == 'Apple' or data == 'ASUS' or data == 'Xiaomi' or data == 'Honor' or data == 'Acer':
#         laptops = Product.objects.filter(category='L').filter(brand=data)
#     elif data == 'below':
#         laptops = Product.objects.filter(
#             category='L').filter(discounted_price__lt=25000)
#     elif data == 'above':
#         laptops = Product.objects.filter(
#             category='L').filter(discounted_price__gt=25000)
#     return render(request, 'app/laptop.html', {'laptops': laptops})

def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Lenovo' or data == 'HP' or data == 'Dell' or data == 'Apple' or data == 'ASUS' or data == 'Xiaomi' or data == 'Honor' or data == 'Acer':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=25000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=25000)
    return render(request, 'app/laptop.html',{'laptops':laptops})


# def login(request):
#     return render(request, 'app/login.html')


# def customerregistration(request):
#     return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})



def checkout(request):
    return render(request, 'app/checkout.html')
