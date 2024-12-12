from django.contrib import admin
from .models import UserProfile
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Unregister the default UserAdmin
admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'list_groups')  # Add 'list_groups' here
    list_filter = ('groups',)  # Add filter for groups
    ordering = ('username',)  # Sort by username

    def list_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])  # Display group names
    list_groups.short_description = 'Groups'  # Column name in the admin

# Register the customized UserAdmin
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')