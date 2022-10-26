from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import OrderDetail, Product
from django.contrib.auth.decorators import login_required
# for class based view importing start here
from django.views.generic import ListView, DetailView,TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
#Funtion view paginator
from django.core.paginator import Paginator
# Payment Gateway
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import stripe



def index(request):
    return HttpResponse("Hello World")


def products(request):
    products = Product.objects.all()
    #Funtion view paginator
    paginator = Paginator(products,3)
    page_number = request.Get.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj
    }
    return render(request, 'myapp/index.html',context)

#Class based view for above products view [ListView]
class ProductListView(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'products'
    #Class view paginate item by 3, if want to 10 just replace 3 to 10
    paginate_by = 3


# Function view Product detail page view code
def product_detail(request,id):
    product = Product.objects.get(id=id)
    context = {
            'product':product
        } 
    return render(request, 'myapp/detail.html',context)

#Class based view for above products_details view [DetailView]
class ProductDetailView(DetailView):
    model = Product
    template_name = 'myapp/detail.html'
    context_object_name = 'product'
    #Payment gateway
    pk_url_kwarg = 'pk'

    def get_context_data(self,**kwargs):
        context = super(ProductDetailView,self).get_context_data(**kwargs)
        context['stripe_publisahble_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

    
@login_required
# Add Function page
def add_product(request):
    
    if request.method =='POST':

        Name = request.POST.get('Name')
        Brand = request.POST.get('Brand')
        Description = request.POST.get('Description')
        Stock = request.POST.get('Stock')
        SupplierPrice = request.POST.get('SupplierPrice')
        SRP = request.POST.get('SRP')
        image = request.FILES['upload']
        seller_name = request.user
        product = Product(Name=Name,Brand=Brand,Description=Description,Stock=Stock,SupplierPrice=SupplierPrice,SRP=SRP,image=image,seller_name=seller_name)
        product.save()
        return redirect('/users/profile')
    return render(request, 'myapp/addproduct.html')


# Class based view for adding/creating new product
class ProductCreateView(CreateView):
    model = Product
    fields = ['Name','Brand','Description','Stock','SupplierPrice','SRP','image','seller_name']
    #success_url = reverse_lazy('myapp:products')
    #product_form.html


@login_required
# Function view for update product
def update_product(request,id):
    product = Product.objects.get(id=id)
    if request.method=='POST':
        product.Name = request.POST.get('Name')
        product.Brand = request.POST.get('Brand')
        product.Description = request.POST.get('Description')
        product.Stock = request.POST.get('Stock')
        product.SupplierPrice = request.POST.get('SupplerPrice')
        product.SRP = request.POST.get('SRP')
        product.image = request.FILES['upload']
        product.save()
        return redirect('/myapp/products')
    context= {
        'product':product,
    }
    return render(request,'myapp/updateproduct.html',context)

# Class based view for updating product
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['Name','Brand','Description','Stock','SupplierPrice','SRP','image','seller_name']
    #Create tempalte on different name of htm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('myapp:mylistings')


@login_required
def delete_product(request,id):
    product = Product.objects.get(id=id)
    context = {
        'product':product,
    }
    if request.method =='POST':
        product.delete()
        return redirect('/myapp/products')
    return render(request,'myapp/delete.html',context)


# Class based view for deleting product
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('myapp:mylistings')


@login_required
def my_listings(request):
    products = Product.objects.filter(seller_name=request.user)
    context = {
        'products':products,
    }
    return render(request,'myapp/mylistings.html',context)


#payment gateway
@csrf_exempt
def create_checkout_session(request,id):
    product = get_object_or_404(Product,pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = request.user.email,
        
        payment_method_types=['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'usd',
                    'product_data':{
                        'name':product.name,
                    },
                    'unit_amount':int(product.price *100),
                },
                'quantity':1,
            }
        ],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('myapp:success'))+"?session_id={CHECKOUT_SESSION_ID}",
        cancel_url= request.build_absolute_uri(
            reverse('myapp:failed')),
    )
    
    order = OrderDetail()
    order.customer_username = request.user.username
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price*100)
    order.save()
    return JsonResponse({'sessionId':checkout_session.id})

class PaymentSuccessView(TemplateView):
    template_name ='myapp/payment_success.html'
    
    def get(self,request,*args,**kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        session = stripe.checkout.Session.retrieve(session_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = get_object_or_404(OrderDetail,stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request,self.template_name)
    
class PaymentFailedView(TemplateView):
    template_name = 'myapp/payment_failed.html'
