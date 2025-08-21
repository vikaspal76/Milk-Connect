from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages,auth
from .models import *
from django.contrib.auth.decorators import login_required
import random
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F,Sum
from datetime import date
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, FloatField
def homepage(request):
    _extra_milk=Extra_Milk_Today.objects.filter(date=date.today(),status="stock")
    extra_milk=[]
    milkmen_list = Milkman.objects.all().order_by('name')
    for i in _extra_milk:
        try:
            pic=Milkman.objects.get(username=i.milkman_username).pic
        except:
            pic=None
       
        extra_milk.append({
        "milkman_username":i.milkman_username,
        "milkman_name":i.milkman_name,
        "quantity":i.quantity,
        "amount":i.amount,
        "animal_type":i.animal_type,
        "pic":pic
        })
    if request.user.is_authenticated:
        usertype = Milkman.objects.filter(username=request.user.username)
    else:
        usertype = None  # or handle anonymous user

    if(request.method=="POST"):
        search=request.POST.get("search")
        type=request.POST.get("type")
        if search:
            milkmen_list = Milkman.objects.filter(Q(name__icontains=search) | Q(city__icontains=search))
        if type:
            milkmen_list=milkmen_list.filter(Q(milktype__icontains=type))

    

    paginator = Paginator(milkmen_list, 3)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Send page_obj as 'data' so your template uses data as usual
    return render(request, "index.html", {"data": page_obj,"usertype":usertype,"extra_milk":extra_milk})

def loginpage(request):
    if (request.method=="POST"):
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            # at this point can we want which user is login user is login 
            try:
                costumer=Costumer.objects.get(username=username)
                # redirect to  costumer profile
                return redirect("/costumer-dashboard/")

            except Costumer.DoesNotExist:
                # difinately he is milkman redirect to milkman dashboard
                return redirect("/dashboard/")
                            
        else:
            messages.error(request,"Invalid username and password")
                                        

    return render(request,"login.html")
@login_required()
def milkman_dashbord(request):
    milkman = request.user.username
    objmilkman=Milkman.objects.get(username=milkman)
    mtype =objmilkman .milktype
    customer = Costumer.objects.filter(costumer_milkman=milkman,custumer_request="Accept")
    total = customer.count()
    record = DailyRecord.objects.filter(date=timezone.now().date(), milkman_username=milkman)
    pending=Costumer.objects.filter(custumer_request="Pending",costumer_milkman=milkman)

    total_pending=pending.count()
    print(total_pending)
    
    total_milk = record.aggregate(
        total=Sum((F("delivered_qty") + F("extra_qty")))
    )["total"]
    print(total_milk)
    extra_milk=Extra_Milk_Today.objects.filter(milkman_username=request.user.username)
    print(extra_milk)
    past_data_milkaman=None
    

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        date_str = request.POST.get("date")
        entry_date = parse_date(date_str) if date_str else timezone.now().date()
        if form_type=="today_entry":
            for c in customer:
                delivered_qty = request.POST.get(f"delivered_qty_{c.username}")
                extra_qty = request.POST.get(f"extra_qty_{c.username}")
                status = request.POST.get(f"status_{c.username}")
                notes = request.POST.get(f"notes_{c.username}")

                delivered_qty = float(delivered_qty) if delivered_qty else 0
                extra_qty = float(extra_qty) if extra_qty else 0

                DailyRecord.objects.update_or_create(
                    date=entry_date,
                    milkman_username=milkman,
                    customer_username=c.username,
                    defaults={
                        "delivered_qty": delivered_qty,
                        "extra_qty": extra_qty,
                        "status": status,
                        "notes": notes if notes else ""
                    }
                )
        elif (form_type == "extra_milk"):
            extraobj= Extra_Milk_Today()
            extraobj.date=date.today()
            extraobj.milkman_username=milkman
            extraobj.milkman_name=objmilkman.name
            extraobj.quantity=request.POST.get("quantity")
            extraobj.amount=request.POST.get("amount")
            extraobj.animal_type=request.POST.get("animal_type")
            extraobj.save()
            messages.success(request,"today extra milk entered")
        else:
            pastdate=request.POST.get("pastdate")
            past_data_milkaman = DailyRecord.objects.filter(date=pastdate, milkman_username=milkman)


    return render(
        request,
        "milkmandashboard.html",
        {"customer": customer, "mtype": mtype, "record": record, "total": total, "total_milk": total_milk,"extra_milk":extra_milk,"total_pending":total_pending,"past_data_milkaman":past_data_milkaman}
    )

from django.shortcuts import get_object_or_404

def coustumer_signup(request, id):
    milkman=Milkman.objects.get(id=id)
    if(request.method=="POST"):
        
        username = request.POST.get("username")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        email = request.POST.get("email")
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another one.")
            return redirect("/costumer-signup/"+str(id))  # Stop here, don't create user

        # Check if passwords match
        if password != cpassword:
            messages.error(request, "Password and confirm password do not match")
            return redirect("/costumer-signup/"+str(id))  # Stop here

        # Create Django User
        user = User.objects.create_user(username=username, password=password,email=email)
        user.save()

        # Create costumer profile
        costumer = Costumer()
        costumer.name = request.POST.get("name")
        costumer.username = username
        costumer.email = request.POST.get("email")
        costumer.phone = request.POST.get("phone")
        costumer.addressline = request.POST.get("addressline")
        costumer.city = request.POST.get("city")

        if request.FILES.get("pic"):
            costumer.pic = request.FILES.get("pic")

        costumer.costumer_milkman =milkman.username
        costumer.quantiy_liter=request.POST.get("quantiy_liter")
        costumer.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("/")  # Redirect to login or homepage

    return render(request, "signup_costumer.html", {"milkman": milkman})


def logout(request):
    auth.logout(request)
    return  redirect("/")

def forget_pass(request):
    if request.method=="POST":
        username=request.POST.get("username")
        try:
            user=Milkman.objects.get(username=username)
           
            otp=str(random.randint(1000,9999))
            messages.success(request,f"otp send on {user.email} ")
            request.session["otp"]=otp
            request.session["username"]=username
            try:
                send_mail(
                    subject="Your OTP Code",
                    message=f"Your OTP is {otp}. It will expire in 5 minutes.",
                    from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                return redirect("/otp/")
                
            except Exception as e:
                return HttpResponse(f"❌ Error sending OTP: {e}")
            
            
        except  Milkman.DoesNotExist:
            messages.error(request,"User does not exit or wrong username")
    return render(request,"forget.html")



def resendotp(request):
    username = request.session.get("username")
    if not username:
        messages.error(request, "⚠️ No user session found. Please start again.")
        return redirect("/forget-password/")  # your forget password URL

    otp=str(random.randint(1000,9999))
    request.session["otp"]=otp   #update with new otp
    request.session["username"]=username


    try:
        user = Milkman.objects.get(username=username)
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is {otp}. Generated at . It will expire in 5 minutes.",
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
            recipient_list=[user.email],
            fail_silently=False,
        )
        messages.success(request, "✅ A new OTP has been sent to your email.")
        return redirect("/otp/")

    except User.DoesNotExist:
        messages.error(request, "⚠️ User not found.")
        return redirect("/forget-password/")

    except Exception as e:
        return HttpResponse(f"❌ Error sending OTP: {e}")

def otp_verification(request):
    if (request.method=="POST"):
        userotp=request.POST.get("otp")
        emailotp=request.session.get("otp")
        if(userotp==emailotp):
           print("success")
           messages.success(request,"set new password")
           return redirect("/set-pasword/")
        else:
            print("invalid otp")
            messages.error(request,"otp  not match")
    return render(request,"otp_verify.html")

def set_password(request):
    if request.user.is_authenticated:
        usertype = Milkman.objects.filter(username=request.user.username)
    else:
        usertype = None  # or handle anonymous user

    if(request.method=='POST'):
        password=request.POST.get("password")
        cpassword=request.POST.get("cpassword")
        if(password==cpassword):
            try:
                username=request.session.get("username")
                user=User.objects.get(username=username)
                user.set_password(password)
                user.save()
                print("password change succesfully")
                return redirect("/login/")
            except User.DoesNotExist:
                messages.error(request,"session expire")

        else:
            messages.error(request,"password and confrim password do not match")
    return render(request,"set-password.html",{"usertype":usertype})




def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        email = request.POST.get("email")
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another one.")
            return redirect("/sign-up/")  # Stop here, don't create user

        # Check if passwords match
        if password != cpassword:
            messages.error(request, "Password and confirm password do not match")
            return redirect("/sign-up/")  # Stop here

        # Create Django User
        user = User.objects.create_user(username=username, password=password,email=email)
        user.save()

        # Create Milkman profile
        milkman = Milkman()
        milkman.name = request.POST.get("name")
        milkman.username = username
        milkman.email = request.POST.get("email")
        milkman.phone = request.POST.get("phone")
        milkman.addressline = request.POST.get("addressline")
        milkman.city = request.POST.get("city")

        if request.FILES.get("pic"):
            milkman.pic = request.FILES.get("pic")

        milkman.milktype = request.POST.get("milktype")
        milkman.price_per_liter = request.POST.get("price_per_liter")
        milkman.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("/login/")  # Redirect to login or homepage

    return render(request, "signup.html")

def details_milkman(request, num):
    milkman = Milkman.objects.get(id=num)

    try:
        dairy = Dairyimages.objects.get(milkman_username=milkman.username)
    except Dairyimages.DoesNotExist:
        dairy = None   # handle case when image does not exist

    try:
        ratings = Rating.objects.filter(milkmanuser=milkman.username)
        
    except Rating.DoesNotExist:
        ratings = None   # same for rating if missing

    return render(request, "detail.html", {
        "milkman": milkman,
        "dairy": dairy,
        "ratings": ratings
    })


def changepassword(request):
    if(request.method=="POST"):
        user=User.objects.get(username = request.user.username)
        password=request.POST.get("old_password")
        if check_password(password, user.password):
            new_password=request.POST.get("new_password")
            c_password=request.POST.get("confirm_password")
            if(new_password==c_password):
                user.set_password(new_password)
                user.save()
                messages.success(request,"password updated")
            else:
                messages.error(request,"new password and confrim password do not match")

        else:
            messages.error(request,"wrong password | enter correct old passwword")
    return render(request,"update_password.html")

@login_required()
def costumer_dashboard(request):
    costumers = Costumer.objects.get(username=request.user.username)
    milkman = Milkman.objects.get(username=costumers.costumer_milkman)
    request_status=costumers.custumer_request
    print(request_status)
    record = DailyRecord.objects.filter(customer_username=request.user.username,status="Delivered",custumer_status="Delivered")
    price = milkman.price_per_liter
    total_milk = record.aggregate(total=Sum(F("delivered_qty") + F("extra_qty")))["total"] or 0
    amount = total_milk * price
    
    today_date = date.today()
   #print("Today's records:", DailyRecord.objects.filter(customer_username=request.user.username).values())
    today = DailyRecord.objects.filter(
    customer_username=request.user.username,
    date=today_date,
    custumer_status__iexact="Notupdated").first()  
    if(today is not None):
         today_total=today.delivered_qty+today.extra_qty
    else:
        today_total=0
    
    

    # ✅ Past records exclude Notupdated and today
    past_data = DailyRecord.objects.filter(
        customer_username=request.user.username
    ).exclude(custumer_status="Notupdated").order_by("-date")
   

    past_data = [
        {
            "date": rec.date,
            "milkman_username": rec.milkman_username,
            "total_milk": rec.delivered_qty + rec.extra_qty,
            "status": rec.status,
            "costumer_status": rec.custumer_status,
        }
        for rec in past_data
    ]

    return render(request, "costumer_dashboard.html", {
        "total_milk": total_milk,
        "price": price,
        "amount": amount,
        "today": today,
        "past_data": past_data,
        "today_date": today_date,
        "today_total":today_total,
        "request_status":request_status
    })


def payment_page(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Get customer and milkman
    customer = Costumer.objects.get(username=request.user.username)
    milkman = Milkman.objects.get(username=customer.costumer_milkman)
    
    # Get daily records
    record = DailyRecord.objects.filter(
        customer_username=request.user.username,
        status="Delivered",
        custumer_status="Delivered"
    )
    
    # Calculate total milk
    total_milk = record.aggregate(
        total=Sum(F("delivered_qty") + F("extra_qty"))
    )["total"] or 0
    
    # Multiply by price and convert to paise (integer)
    price = milkman.price_per_liter
    amount = int(total_milk * price * 100)  # ✅ convert Decimal to int
    
    # Create Razorpay order
    DATA = {
        "amount": amount,       # must be int
        "currency": "INR",
        "payment_capture": 1
    }
    order = client.order.create(data=DATA)
    
    context = {
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "order_id": order["id"],
        "amount": amount,
        "phone":customer.phone,
        "email":customer.email
    }
    
    return render(request, "payment.html", context)



@csrf_exempt
def payment_success(request):
    return HttpResponse("✅ Payment Successful! Thank you.")


def discout(request):
    if(request.method=="POST"):
        email=request.POST.get("email")
        user=Discount()
        user.email=email
        user.save()
        messages.success(request,"thank you for Subscribe")
        return redirect("/")
    return redirect("/")


def confrim_custumer(request):
    if(request.method=="POST"):
        status=request.POST.get("status_today")
        today = date.today()
        today_entry = DailyRecord.objects.filter(
            customer_username=request.user.username,
            date=today
        ).first()
        today_entry.custumer_status=status  
        today_entry.save()      
        messages.success(request," ✅status updates succesfully")
    return redirect("costumer_dashboard")   #  matches urls.py


def new_request_(request):
    new_request = Costumer.objects.filter(costumer_milkman=request.user.username,custumer_request="Pending")
    print(new_request.count())
    return render(request,"updaterequest.html",{"new_request":new_request})

def modify_request(request,id):
    if(request.method=="POST"):
        status=request.POST.get("request")
        cutumer=Costumer.objects.get(id=id)
        cutumer.custumer_request=status
        cutumer.save()
        return redirect("/dashboard/")
def milkstate(request,id):
    if(request.method=="POST"):
        change=request.POST.get("Change")
        extra=Extra_Milk_Today.objects.get(id=id)
        if change=="out of stock":
            extra.status="out of stock"
            extra.save()
        else:
            extra.delete()
    return redirect("/dashboard/")

def aboutpage(request):
    return render(request,"about.html")


def feedbackform(request):
    custumer=Costumer.objects.get(username=request.user.username)

    if(request.method=="POST"):
        rating=request.POST.get("rating")
        feedback=request.POST.get("feedback")
        new_rating=Rating()
        new_rating.customeruser=request.user.username
        new_rating.value=rating
        new_rating.review=feedback
        new_rating.milkmanuser=custumer.costumer_milkman
        new_rating.save()
        return redirect("/costumer-dashboard/")
    
def updateprofilemilkman(request):
    milkman = Milkman.objects.get(username=request.user.username)
    dairy, created = Dairyimages.objects.get_or_create(
        milkman_username=milkman.username
    )

    if request.method == "POST":
        # Update Milkman info
        milkman.name = request.POST.get('name')
        milkman.email = request.POST.get('email')
        milkman.phone = request.POST.get('phone')
        milkman.city = request.POST.get('city')
        milkman.addressline = request.POST.get('addressline')
        milkman.milktype = request.POST.get('milktype')
        milkman.price_per_liter = request.POST.get('price_per_liter')

        if request.FILES.get('pic'):
            milkman.pic = request.FILES['pic']

        milkman.save()

        # Update Dairy Images
        for i in range(1, 5):
            file = request.FILES.get(f'pic{i}')
            if file:
                # Delete previous file if exists
                old_file = getattr(dairy, f'pic{i}')
                if old_file:
                    old_file.delete(save=False)
                setattr(dairy, f'pic{i}', file)

        dairy.save()
        return redirect("/dashboard/")

        
    return render(request, 'updateprofile.html', {'milkman': milkman, 'dairy': dairy})

def placeorder(request):
    return render(request,"orderplace.html")

















