from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    
    # This adds the 'role' field to the edit screen
    fieldsets = UserAdmin.fieldsets + (
        ('Role Management', {'fields': ('role',)}),
    )
    # This adds the 'role' field to the creation screen
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Management', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)