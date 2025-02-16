# meditatii/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Meditation


@admin.register(Meditation)
class MeditationAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'date', 'payment_amount', 'payment_status')
    list_filter = ('payment_status', 'date', 'teacher')
    search_fields = ('student__username', 'teacher__username')
    date_hierarchy = 'date'


# admin.py
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'nume_real', 'email', 'cnp_cui', 'phone_number', 'company_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    search_fields = ('username', 'cnp_cui', 'phone_number', 'company_name', 'nume_real', 'email')

    fieldsets = (
        *UserAdmin.fieldsets,
        ('User Profile', {
            'fields': ('user_type', 'cnp_cui', 'nume_real', 'phone_number', 'company_name',)
        })
    )
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        ('User Profile', {
            'fields': ('user_type', 'cnp_cui', 'nume_real', 'phone_number', 'company_name', 'email')
        })
    )


admin.site.register(User, CustomUserAdmin)