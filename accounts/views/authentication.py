from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from accounts.decorators.auth import user_not_logged_in
from accounts.models import Profile, OTP
import random
import smtplib
from email.message import EmailMessage
import pyotp
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


@csrf_exempt
@user_not_logged_in
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return JsonResponse({"success": False, "message": "Email and password are required."}, status=400)
        
        # Check if user exists
        user = User.objects.filter(username=email).first()
        if user and user.check_password(password):
            print("valid user")
            auth_login(request, user)
            return JsonResponse({"success": True, "message": "User logged in successfully."})
        else:
            return JsonResponse({"success": False, "message": "Invalid email or password."}, status=400)
    
    context = {
        "hideNav":True
    }
    return render(request, 'login.html', context)

@csrf_exempt
@user_not_logged_in
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        country_code = request.POST.get('country_code')
        email = request.POST.get('email')
        password = request.POST.get('password')
        otp = request.POST.get('otp')

        print(first_name, last_name, phone, country_code, email, password)
    
        if not first_name:
            return JsonResponse({"success": False, "message": "First Name is required."}, status=400)
        if not last_name:
            return JsonResponse({"success": False, "message": "Last Name is required."}, status=400)
        if not email :
            return JsonResponse({"success": False, "message": "Email is required."}, status=400)
        if not phone:
            return JsonResponse({"success": False, "message": "Mobile Number is required."}, status=400)
        if not country_code:
            return JsonResponse({"success": False, "message": "Country Code is required."}, status=400)
        if not password:
            return JsonResponse({"success": False, "message": "Password is required."}, status=400)
        if not otp:
            return JsonResponse({"success": False, "message": "OTP is required."}, status=400)
        
        if User.objects.filter(username=email).exists():
            return JsonResponse({"success": False, "message": "User with this email already exists."}, status=400)
        
        otp_obj = OTP.objects.filter(email=email, otp=otp).first()
        if not otp_obj:
            return JsonResponse({"success": False, "message": "Invalid OTP."}, status=400)
        
        if otp_obj.created_at < timezone.now() - timedelta(minutes=5):
            return JsonResponse({"success": False, "message": "OTP expired."}, status=400)
        
        OTP.objects.filter(email=email, otp=otp).delete()
        
        # Check if user exists
        user = User.objects.create_user(username=email,email=email, first_name=first_name, last_name=last_name, password=password)
        Profile.objects.create(
            user=user,
            country_code=country_code,
            mobile_no=phone
        )
        auth_login(request, user)
        return JsonResponse({"success": True, "message": "User logged in successfully."})
    
    context = {
        "hideNav":True
    }
    return render(request, 'signup.html', context)

@csrf_exempt
def logout(request):
    auth_logout(request)
    return redirect('home')


@csrf_exempt
def send_otp(request):
    email = request.POST.get('email')
    if not email:
        return JsonResponse({"success": False, "message": "Email not provided."})

    # Generate a secure 6-digit OTP using pyotp library
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)  # 5 minute validity
    otp = totp.now()
    OTP.objects.create(email=email, otp=otp)
    
    print(f"Sending OTP {otp} to email: {email}")

    # Store the OTP in the session (or save it in the database as needed)
    request.session['otp'] = otp

    # Compose the email message
    # Compose the email message with HTML formatting
    msg = EmailMessage()
    msg.set_content(f"""
    Dear User,

    Your One-Time Password (OTP) for verifying your email and completing your signup on TicketClue (a platform by Travel Pae Private Limited) is:

    {otp}

    This OTP is valid for 5 minutes. Please do not share it with anyone.

    Thank you for choosing TicketClue!

    Best regards,  
    The TicketClue Team
    """)

    msg.add_alternative(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
            }}
            .container {{
                max-width: 500px;
                background: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }}
            .otp-code {{
                font-size: 32px;
                font-weight: bold;
                color: #484848;
                margin: 20px 0;
                display: inline-block;
                padding: 10px;
                background: #f9f9f9;
                border-radius: 5px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>TicketClue OTP Verification</h2>
            <p>Your One-Time Password (OTP) for verifying your email and completing your signup on <strong>TicketClue</strong> (a platform by <strong>Travel Pae Private Limited</strong>) is:</p>
            <div class="otp-code">{otp}</div>
            <p>This OTP is valid for <strong>5 minutes</strong>. Please do not share it with anyone.</p>
            <p>Thank you for choosing TicketClue!</p>
            <div class="footer">If you did not request this, please ignore this email.</div>
        </div>
    </body>
    </html>
    """, subtype="html")

    msg['Subject'] = "Your TicketClue OTP Code"
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = email


    try:
        if settings.EMAIL_USE_SSL:
            smtp_server = smtplib.SMTP_SSL(settings.EMAIL_HOST, 465)  # Use SSL and port 465
        else:
            smtp_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            smtp_server.starttls()  # Secure the connection if not using SMTP_SSL
        smtp_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp_server.send_message(msg)
        smtp_server.quit()

        print(f"OTP sent successfully to {email}")
        return JsonResponse({"success": True, "message": "OTP sent successfully."})
    except Exception as e:
        print(f"Error sending OTP: {str(e)}")
        return JsonResponse({"success": False, "message": "Failed to send OTP."})

