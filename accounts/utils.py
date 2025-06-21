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
    
def send_email_verfication(request,user,mail_subject,email_template):
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user)
    })

    to_email = user.email
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        mail.send()
    except Exception as e:
        print(f"Error sending email: {e}")   

def send_notification(mail_template,context,mail_subject):
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email=context['user'].email
    message=render_to_string(mail_template,context)
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
