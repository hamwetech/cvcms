from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from .models import User
#
# from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
# from unfold.admin import ModelAdmin
#
#
# admin.site.unregister(User)
# admin.site.unregister(Group)
#
#
# @admin.register(User)
# class UserAdmin(BaseUserAdmin, ModelAdmin):
#     # Forms loaded from `unfold.forms`
#     form = UserChangeForm
#     add_form = UserCreationForm
#     change_password_form = AdminPasswordChangeForm
#
#
# @admin.register(Group)
# class GroupAdmin(BaseGroupAdmin, ModelAdmin):
#     pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'msisdn', 'access_level', 'is_active', 'is_superuser')
    list_filter = ('is_active', 'is_superuser', 'access_level', 'district')
    search_fields = ('email', 'first_name', 'last_name', 'msisdn', 'nin')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_photo', 'sex', 'date_of_birth', 'msisdn', 'nin')}),
        ('Location', {'fields': ('district', 'county', 'sub_county', 'parish', 'village', 'gps_coodinates', 'district_incharge')}),
        ('System Info', {'fields': ('access_level', 'supervisor', 'is_supervisor', 'is_locked', 'receive_sms_notifications', 'otp_secret')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # ('Important Dates', {'fields': ('last_login', 'create_date', 'update_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )