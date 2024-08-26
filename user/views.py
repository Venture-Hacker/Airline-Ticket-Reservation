from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            # Check if the email or username already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=fname,
                    last_name=lname,
                    password=password
                )
                user.save()

                # Log in the user after registration
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')  # Redirect to your home page or another page
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate using the provided credentials
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to your home page or another page
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'login.html')


@login_required
def dashboard(request):
    user_first_name = request.user.first_name
    return render(request, 'dashboard.html', {'first_name': user_first_name})


def logout_view(request):
    auth_logout(request)
    return redirect('login')
