from django.contrib import admin
from .models import * 
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Cheese)
admin.site.register(Crust)
admin.site.register(Sauce)
admin.site.register(Size)
admin.site.register(User, UserAdmin)
admin.site.register(Pizza)
admin.site.register(Orders)