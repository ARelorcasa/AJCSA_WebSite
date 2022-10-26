from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from myapp.models import Product



def register(request):
    if request.method =='POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request,'users/login.html')
    form = NewUserForm()
    context={
        'form':form,
    }
    return render(request,'users/register.html',context)
    
# authenticator for pages @login_required
@login_required
def profile(request):
    products = Product.objects.filter(seller_name=request.user)
    context={
        'products':products,
        }
    return render(request,'users/profile.html',context)

@login_required
def create_profile(request):
    if request.method == 'POST':
        contact_number = request.POST.get('contact_number')
        image = request.FILES['upload']
        user = request.user
        profile = Profile(user=user,image=image,contact_number=contact_number)
        profile.save()
        return redirect('/users/profile')
    return render(request,'users/createprofile.html')

    # for Seller Profie, to see Profile of Seller
def seller_profile(request,id):
    
    seller = User.objects.get(id=id)
    #products = Product.objects.get_queryset(seller_name_id=request.user)
    context={
        'seller':seller,
        #'products':products,
        }
    return render(request,'users/sellerprofile.html',context)