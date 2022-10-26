from django.contrib import admin
from django.urls import path
from . import views

app_name='myapp'


urlpatterns = [
    path('', views.index),
    path('products/', views.ProductListView.as_view(),name='products'),
    #product details page according to ID of an item
    path('products/<int:pk>', views.ProductDetailView.as_view(),name='product_detail'),
    #URL page for adding products
    path('products/add/', views.add_product,name='add_product'),
    #This is Sample of function Class view:path('products/add/', views.ProductCreateView.as_view(),name='add_product'),
    #URL page for updating products according to its ID INT is for function view PK is for Create view
    path('products/update/<int:pk>/',views.ProductUpdateView.as_view(),name='update_product'),
    #URL page for deleting products according to its ID
    path('products/delete/<int:pk>/',views.ProductDeleteView.as_view(),name='delete_product'),
    path('products/mylistings',views.my_listings,name='mylistings'),
    path('success/',views.PaymentSuccessView.as_view(),name='success'),
    path('failed/',views.PaymentFailedView.as_view(),name='failed'),
    path('api/checkout-session/<id>',views.create_checkout_session,name='api_checkout_session'),
]

