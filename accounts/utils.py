from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from FoodOnline_main import settings

def detectuser(user):
    if user.role == 1:
        user_url="vend_dashboard"
        return user_url
    elif user.role == 2:
        user_url="cust_dashboard"
        return user_url
    elif user.role == None and user.is_superadmin:
        user_url = "/admin"
        return user_url
    
def send_email_verfication(request, user):
    current_site = get_current_site(request)
    mail_subject = "FooodOnline Account Verification"
    
    message = render_to_string("email/account_verfication.html", {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user)
    })

    to_email = user.email
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        print(f"Sending verification email to: {to_email}")
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        mail.send()
    except Exception as e:
        print(f"Error sending email: {e}")    

def send_forgot_password_email(request,user):
    current_site = get_current_site(request)
    mail_subject = "FooodOnline Forgot Password"
    
    message = render_to_string("email/forgot_email.html", {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user)
    })

    to_email = user.email
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        print(f"Sending verification email to: {to_email}")
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        mail.send()
    except Exception as e:
        print(f"Error sending email: {e}") 
