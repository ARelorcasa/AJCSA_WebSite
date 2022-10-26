from django.contrib import admin
#Register apps/table to admin site
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','contact_number','image')


admin.site.register(Profile, ProfileAdmin)

