from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
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

        # * Here is will check the user if the user is register in the database but the account is not active then 
        # * It will only send the activation link to the specified email
        if(Account._default_manager.get(email=email, is_active=False)):
            user = Account._default_manager.get(email=email, is_active=False)
            try:
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
                return JsonResponse({'success': f"Activation Email has been sent to your Email."}, safe=False)
            except:
                return JsonResponse({'error': f"Activation Email Has Not Been Sent"}, safe=False)
        
        # * Here it will try to create the user with the specified data if there is some error it will send the error message
        # * Other wise it will go to next Account Activation step
        else:        
            try:
                user = Account.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                user.save()
                # * If the user is successfully store in the database then it will tyr to send activation link 
                # * if there is some error it will send back the error message other wise send the success message to the user
                try:
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
                    return JsonResponse({'success': f"Activation Email has been sent to your Email."}, safe=False)
                except:
                    return JsonResponse({'error': f"Activation Email Has Not Been Sent"}, safe=False)
            except:
                return JsonResponse({'error': f"Email has been already taken"}, safe=False)


    # * This will return if the request method is GET 
    return render(request, "index.html")




def activate(request, uidb64, token):
    # * In the Activation link will there is encoded primary key of that user and token
    # * so here try to encode the primary key and get the user form the database
    #  * if the user us not present in the database then user == None
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    # * if the user is present then we will check token and activate the user Account 
    # * if token is invalid then we will redirect the user back to registration page and send invalid link message
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f"Account has been created for {user.first_name}")
        return redirect("/login")
    else:
        messages.error(request, f"Invalid Activation Link")
        return redirect('/')




def login(request):
    return render(request, 'login.html')