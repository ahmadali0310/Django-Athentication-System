from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ("username","first_name", 'last_name', 'email')

    list_filter = ()
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)