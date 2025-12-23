import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Customer

def sign_up(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # ✅ BASIC VALIDATIONS
        if not full_name or not email or not phone or not password:
            messages.error(request, "All fields are required!")
            return redirect("sign_up")

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters!")
            return redirect("sign_up")

        if not re.match(r'^\d{10}$', phone):
            messages.error(request, "Enter valid 10 digit mobile number!")
            return redirect("sign_up")

        if "@" not in email:
            messages.error(request, "Enter valid email!")
            return redirect("sign_up")

        # ✅ VERY IMPORTANT STEP
        # Make ALL users inactive first
        Customer.objects.update(current_user='F')

        # ✅ CREATE NEW USER AS ACTIVE
        user = Customer.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            password=password,
            current_user='P'
        )

        # ✅ SEND EMAIL
        try:
            send_mail(
                subject='Welcome to Our Site!',
                message=f'Hi {full_name},\n\nYour account has been successfully created!',
                from_email='bdada3038@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            messages.warning(request, "Account created but email not sent")

        messages.success(request, "Account Created Successfully! Please Login.")
        return redirect("sign_in")

    return render(request, "accounts/sign_up.html")



def sign_in(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        password = request.POST.get("password")

        try:
            user = Customer.objects.get(full_name=full_name, password=password)

            # ✅ Reset all users to N first
            Customer.objects.exclude(id=user.id).update(current_user='N')

            # ✅ Set current user to P
            user.current_user = 'P'
            user.save(update_fields=['current_user'])

            # ✅ Session for future use (optional)
            request.session["customer_id"] = user.id

            messages.success(request, "Login Successful!")
            return redirect("profile")  # redirect to profile page

        except Customer.DoesNotExist:
            messages.error(request, "Invalid Name or Password")

    return render(request, "accounts/sign_in.html")


def profile(request):
    user = Customer.objects.filter(current_user='P').first()
    message = None

    if not user:
        message = "Please login to see your details."

    if request.method == "POST" and user:
        if 'logout' in request.POST:
            user.current_user = 'N'
            user.save(update_fields=['current_user'])
            return redirect('sign_in')

    return render(request, "accounts/profile.html", {
        "user": user,
        "message": message
    })



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer

def re_pass(request):
    # Get current logged-in user
    user = Customer.objects.filter(current_user='P').first()
    if not user:
        messages.error(request, "Please login first!")
        return redirect('sign_in')

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if old_password != user.password:
            messages.error(request, "Old password is incorrect!")
        elif new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match!")
        else:
            user.password = new_password
            user.save(update_fields=['password'])
            messages.success(request, "Password updated successfully!")
            return redirect('profile')

    return render(request, "accounts/re_pass.html", {'user': user})
