from urllib import request
import json
from django.forms import TypedMultipleChoiceField
from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login ,logout

from . models import Mens as mensboy
from . models import detailsqr as detailsqrhai
from . models import order as Orderdone
# from . models import Mens,Womens,Kids as AllProducts


# Create your views here.
def Home1(request):
    return render(request,"homepage/index.html")

def Signin(request):
    return render(request,"homepage/signin.html")

def Signindo(request):
    if request.method == "POST":
        username = request.POST.get("email")
        email= username
        pass1= request.POST.get("password")
        pass2= request.POST.get("confirm_password")
        first_name = request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        
        # validationssssss
        if (User.objects.filter(username=username).exists()): 
            # messages.add_message(request, messages.INFO, 'Username already exist.')
            return redirect("/signin/")           
            

        if(not(len(pass1)>7 and not pass1.isalnum())):
            # messages.add_message(request, messages.INFO, 'Password must belonger then 8 characters and should contain a symbol.')
            return redirect("/signin/")
        
        if(not(pass1==pass2)):
            # messages.add_message(request, messages.INFO, 'Both the password must be same.')
            return redirect("/signin/")

        else:
            try:
                newUser = User.objects.create_user(username,email,pass1)
                newUser.first_name = first_name
                newUser.last_name = last_name
                newUser.save()
                # messages.add_message(request, messages.SUCCESS, 'Account succsessfully Created. Please Login to continue.')
                return redirect("/login/")
            except Exception as e:
                # messages.add_message(request, messages.ERROR, e)
                return redirect("/signin/")            
    else:
        # messages.add_message(request, messages.ERROR, 'Please SignIn.')
        return redirect("/login/")



def Login(request):
    return render(request,"homepage/login.html")

def Logindo(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(username = username , password = password )

        if user is not None:
            login(request,user)
            # messages.add_message(request, messages.SUCCESS, 'LOGIN successfull!!')
            return redirect("/")

        else:
            # messages.add_message(request, messages.ERROR, 'Email or password is not valid. ')
            return redirect("/login/")
    else:
        # messages.add_message(request, messages.ERROR, 'Please Login.')
        return redirect("/login/")
    
def logoutkaro(request):
    logout(request)
    # messages.add_message(request, messages.SUCCESS, 'Logout successful')
    return redirect("/")




def Mens(request):
    Mens_products=mensboy.objects.all()
    params = {
        "data":Mens_products
    }
    
    
    return render(request,"homepage/mens.html",params)


def Womens(request):
    Womens_products=mensboy.objects.all()
    params = {
        "data":Womens_products
    }
    return render(request,"homepage/womens.html",params)
    

def Kids(request):
    Kids_products=mensboy.objects.all()
    params = {
        "data":Kids_products
    }
    return render(request,"homepage/kids.html",params)


def Accessories(request):
    Accessories_products=mensboy.objects.all()
    params = {
        "data":Accessories_products
    }
    return render(request,"homepage/Accessories.html",params)




def Detail_mens(request,id):
    # name = request.GET.get("id")

    try:
        params = {"data":mensboy.objects.get(id=id),"error":"null"}
    except:
        params = {"data":{},"error":"Product not found"}

    return render(request,"homepage\details_mens.html",params)


def Detail_womens(request,id):
    # name = request.GET.get("id")

    try:
        params = {"data":mensboy.objects.get(id=id),"error":"null"}
    except:
        params = {"data":{},"error":"Product not found"}

    return render(request,"homepage\details_womens.html",params)

    

def Detail_kids(request,id):
    # name = request.GET.get("id")

    try:
        params = {"data":mensboy.objects.get(id=id),"error":"null"}
    except:
        params = {"data":{},"error":"Product not found"}

    return render(request,"homepage\details_kids.html",params)
    

def Detail_accessories(request,id):
    # name = request.GET.get("id")

    try:
        params = {"data":mensboy.objects.get(id=id),"error":"null"}
    except:
        params = {"data":{},"error":"Product not found"}

    return render(request,"homepage\details_accessories.html",params)



def Cartpage(request):
    return render(request,"homepage/cart.html")



def Checkout(request):
    str = request.POST.get("cartJson")
    cart = json.loads(str)
    currentCart = cart

    
    totalPrice = 0 
    for id in cart:
        temp= cart[id]
        # tempOb0 = mensboy.objects.get(id=id)
        tempOb =mensboy.objects.get(id=id)
        # tempOb2 = kidschild.objects.get(id=id)
        # tempOb=tempOb0+tempOb1+tempOb2
        

        price = tempOb.price
        temp["price"]=price
        temp["totalItemPrice"] = price * temp["value"]
        totalPrice = totalPrice + temp["totalItemPrice"]
        currentCart[id] = temp 
    
    params = {
        "totalPrice" : totalPrice,
        "data": currentCart
    }
    print("this is cart") 
  

    return render(request,"homepage/checkout.html",params)


def submitcheckout(request):
    if(request.method=="POST"):
        jsonCart= request.POST.get("jsonCart")
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        email= request.POST.get("email")
        address= request.POST.get("address")
        state= request.POST.get("state")
        zip= request.POST.get("zip")
        isSameBillingAddress= request.POST.get("isSameBillingAddress")
        if(isSameBillingAddress=="on"):
            isSameBillingAddress = True
        else:
            isSameBillingAddress = False
        
        CODHai= request.POST.get("CODHai")
        if(CODHai=="on"):
            CODHai = True
        else:
            CODHai = False
        
        UPIHai= request.POST.get("UPIHai")
        if(UPIHai=="on"):
            UPIHai = True
        else:
            UPIHai = False
        


        newOrder = Orderdone(jsonCart=jsonCart,email=email, first_name=first_name ,last_name=last_name,state=state,zip=zip,CODHai=CODHai,UPIHai=UPIHai,address=address,isSameBillingAddress=isSameBillingAddress)
        newOrder.save()

      
        return render(request,"homepage/submitcheckout.html")
    else:
        return HttpResponse("You are on a wrong page. please <a href='/course/list'>Click here</a> to add items")

    return HttpResponse("Thank you")
    # return render(request,"course\contactus.html")




def ContactUs(request):
    return render(request,"homepage/contact.html")



# QR code details submitted section starts
def Qrdetails(request):
    return render(request,"homepage/Qrcodepaymentdetails.html")




def Qrdetailsubmitted(request):
    Name = request.POST.get("Namehai")
    TransactionID = request.POST.get("TransactionID")
    UPINumber = request.POST.get("UPINumber")
    UPIIDHAi = request.POST.get("UPIID")
    Filehai =request.FILES['PaymentScreenshot']
    newContact  =  detailsqrhai(Name=Name,TransactionID=TransactionID,UPINumber=UPINumber,UPIIDHAi=UPIIDHAi,Filehai=Filehai)
    newContact.save()

    return HttpResponse("<h3>Details Submitted please <a href='/'>Click here</a> to go to Homepage keep shoping</h3>")


# QR code details submitted section Ends


    





# Ttemp code
def contactusboi(request):
    return render(request,"homepage/contactus.html")

def Contactsubmit(request):
    Name = request.POST.get("Namehai")
    TransactionID = request.POST.get("TransactionID")
    UPINumber = request.POST.get("UPINumber")
    UPIIDHAi = request.POST.get("UPIID")
    Filehai =request.POST.get("PaymentScreenshot")
    newContact  =  detailsqrhai(Name=Name,TransactionID=TransactionID,UPINumber=UPINumber,UPIIDHAi=UPIIDHAi,Filehai=Filehai)
    newContact.save()
    return HttpResponse("<h1>thanks for the response</h1><a href='/shop'><button style='background-color: #0275d8; color:white; /* Green */ border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px;'>Click here to shop</button></a>")
    
# Ttemp code
