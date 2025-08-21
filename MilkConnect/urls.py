
from django.contrib import admin
from django.urls import path
from Mainapp.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",homepage),
    path('login/',loginpage),
    path("dashboard/",milkman_dashbord),
    path("logout/",logout),
    path("forget-password/",forget_pass),
    path('resendotp/', resendotp, name='resendotp'),
    path("otp/",otp_verification),
    path("set-pasword/",set_password),
    path("sign-up/" ,sign_up),
    path("know-more/<int:num>",details_milkman),
    path("change-pass/",changepassword),
    path("costumer-signup/<int:id>",coustumer_signup),
    path('costumer-dashboard/',costumer_dashboard, name='costumer_dashboard'),
     path("pay/", payment_page, name="payment_page"),
    path("payment-success/", payment_success, name="payment_success"),
    path("offer/",discout),
    path("confirm-milk/",confrim_custumer),
    path("new_request/",new_request_),
    path("modigy_request/<int:id>",modify_request),
    path("milkstate/<int:id>",milkstate, name="milkstate"),
    path("aboutus/",aboutpage),
    path("feedback/",feedbackform),
    path("updateprofile/",updateprofilemilkman),
    path("placeorder/",placeorder),
   ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
