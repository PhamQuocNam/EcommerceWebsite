from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User, Profile

# Create your views here.
def register_view(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.staff_status = False
            new_user.superuser_status = False
            new_user.first_name= form.cleaned_data['first_name']
            new_user.last_name=form.cleaned_data['last_name']
            new_user.Address = form.cleaned_data['address']
            new_user.City = form.cleaned_data['city']
            new_user.Country= form.cleaned_data['country']
            new_user.Phone= form.cleaned_data['phone']
            new_user.save()
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hey {username}, You account was created successfully')
            new_user = authenticate(username= form.cleaned_data['email'],
                                    password = form.cleaned_data['password1'],
                                    )
            
            login(request,new_user)
            return redirect('userauths:sign-in')
    else:
        form = UserRegisterForm(request.POST or None)
    
    context ={
        'form': form
    }
    return render(request, 'userauths/sign-up.html', context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,'You have already logged in')
        return redirect("core:index")

    if request.method =="POST":
        email = request.POST.get("email")
        password = request.POST.get('password')
        user = authenticate(request, email = email, password = password)
        try:
            user = User.objects.get(email=email)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in')
                return redirect("core:index")
            else:
                messages.warning(request, "User does not exist. Create an account.")
        
        except:
            messages.warning(request,f"User with {email} does not exist")
    
    return render(request, 'userauths/sign-in.html')


def logout_view(request):
    logout(request)
    messages.success(request,'You logged out.')
    return redirect("core:index")