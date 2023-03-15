from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import View
from customer.forms import RegistrationForm,LoginForm,ReviewForm
from django.contrib.auth import authenticate,login,logout
from store.models import Products,Cart,Order,Offer,Review
from django.utils.decorators import method_decorator

# Create your views here.
def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"please login to perform the action")
            return redirect("log-in")
        else:
            return fn(request,*args,**kw)
    return wrapper
def sign_out_view(request,*args,**kw):
    logout(request)
    return redirect("log-in")

class SignupView(View):
    def get(self,request,*args,**kw):
        form=RegistrationForm()
        return render(request,"signup.html",{"form":form})
    def post(self,request,*args,**kw):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("log-in")
        else:
            return render(request,"signup.html",{"form":form})

class SigninView(View):
    def get(self,request,*args,**kw):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})

    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"signin.html",{"form":form})

@method_decorator(signin_required,name="dispatch")  
class IndexView(View):
    def get(self,request,*args,**kw):
        qs=Products.objects.all()
        return render(request,"index.html",{"products":qs})

@method_decorator(signin_required,name="dispatch")             
class ProductDetailView(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        qs=Products.objects.get(id=id)
        # rw=Review.objects.filter(id=id)
        return render(request,"product-detail.html",{"product":qs,})
@method_decorator(signin_required,name="dispatch")  
class AddToCartView(View):
    def post(self,request,*args,**kw):
        print(request.POST.get("qty"))

        qty=request.POST.get("qty")
        user=request.user
        id=kw.get("id")
        product=Products.objects.get(id=id)
        Cart.objects.create(products=product,user=user,quantity=qty)
        return redirect("home")
@method_decorator(signin_required,name="dispatch")  
class CartList(View):
    def get(self,request,*args,**kw):
        
        qs=Cart.objects.filter(user=request.user,status="in-cart")
        # total= int(Cart.objects.all().annotate(sum('price')))
        
        return render(request,"cart-list.html",{"cart":qs})
@method_decorator(signin_required,name="dispatch")          
class CartRemoveView(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        Cart.objects.filter(id=id).update(status="cancelled")
        return redirect("home")
# class MakeCartorderView(View):
#     def get(self,request,*args,**kw):
#         return render(request,"checkout.html")

@method_decorator(signin_required,name="dispatch") 
class MakeorderView(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        qs=Cart.objects.get(id=id)
        return render(request,"checkout-single.html",{"carts":qs})
    def post(self,request,*args,**kw):
        user=request.user
        address=request.POST.get("address")
        id=kw.get("id")
        qs=Cart.objects.get(id=id)
        product=qs.products
        pincode=request.POST.get("zip")
        Order.objects.create(user=user,address=address,pincode=pincode,product=product)
        qs.status="order-placed"
        qs.save()
        return redirect("home")
@method_decorator(signin_required,name="dispatch") 
class MyOrderView(View):
    def get(self,request,*args,**kw):
        qs=Order.objects.filter(user=request.user).exclude(status="cancelled")
        return render(request,'order-list.html',{"orders":qs})
@method_decorator(signin_required,name="dispatch") 
class OrderCancelView(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        Order.objects.filter(id=id).update(status="cancelled")
        return redirect("my-order")


@method_decorator(signin_required,name="dispatch") 
class DiscountView(View):
    def get(self,request,*args,**kw):
        qs=Offer.objects.all()
        return render(request,'offer.html',{"offers":qs})
@method_decorator(signin_required,name="dispatch") 
class ReviewCreateView(View):
    def get(self,request,*args,**kw):
        form=ReviewForm()
        return render(request,"review.html",{"form":form})

    def post(self,request,*args,**kw):
        form=ReviewForm(request.POST)
        id=kw.get("id")
        pro=Products.objects.get(id=id)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.product=pro
            form.save()
            return redirect("home")
        else:
            return render(request,"review.html",{"form":form})






