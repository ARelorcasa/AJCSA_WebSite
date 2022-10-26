from django.contrib import admin
from .models import Product, OrderDetail


#Add datails in row Product is model name and Admin is the admin itself
class ProductAdmin(admin.ModelAdmin):
    list_display = ('Name','Brand','seller_name','Stock','SRP')
    search_fields = ('Name','Brand',)

    def set_price_to_zero(self,request,queryset):
        queryset.update(SRP=0)

    def set_stock_to_zero(self,request,queryset):
        queryset.update(Stock=0)

    actions = ('set_price_to_zero','set_stock_to_zero',)
    list_editable = ('Stock','SRP',)

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('product','amount',)
    

admin.site.register(Product, ProductAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.site_header = "AveryJaz Computer Shop and Accessories"
admin.site.site_title = "AJCSA"
admin.site.index_title = "AJCSA Administrator"

