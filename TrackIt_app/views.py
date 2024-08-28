from django.shortcuts import render
from .forms import *

# Create your views here.
def user_login(request):
    return render(request, "user-login.html")

def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #user.set_password(form.cleaned_data['password'])
            #user.date_registered = timezone.now()
            user.save()
            #ShopRate.objects.create(shop_id=shop)
            return redirect('user_login')  
    else:
        form = UserSignupForm()
    return render(request, "user-signup.html", {'form': form})

def system_admin_login(request):
    return render(request, "system_admin/system-admin-login.html")

def director_login(request):
    return render(request, "director-login.html")

def forgot_password(request):
    return render(request, "forgot-password.html")

def new_password(request):
    return render(request, "new-password.html")