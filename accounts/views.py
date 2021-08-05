from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Account
from django.utils.encoding import force_bytes
import json


# * Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.

def index(request):
    # * If the request is POST then it will collect the data from request.POST dict
    if request.method == "POST":
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        email = request.POST.get("email")
        password = request.POST.get("pass")
        username = email.split("@")[0]

        # * Here it will try to create instenc of user if the instenc is successfully created then
        # * it will return the success message else it will return an error message.
        try:
            user = Account.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Please Activate Your Account"
            message = render_to_string("email_verification.html", {
                "user": user,
                "domain": current_site,
                "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return JsonResponse({'success': f"Activation Email has been sent to {email}"}, safe=False)
        except:
            return JsonResponse({'error': f"Email has been already taken"}, safe=False)


    # * This will return if the request method is GET 
    return render(request, "index.html")




def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return JsonResponse({'success': f"Account has been created for {user.first_name}"}, safe=False)
    else:
        return JsonResponse({'error': f"Invalid Activation Link"}, safe=False)
        return redirect('/')