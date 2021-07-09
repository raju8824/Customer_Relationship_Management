from django.contrib import admin
from .models import Lead, Agent, User, UserProfile, Category
# Register your models here.


@admin.register(Lead)
class AdminLead(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'age']


@admin.register(Agent)
class AdminAgent(admin.ModelAdmin):
    list_display = ['id', 'user']


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['id', 'username']


@admin.register(Category)
class AdminUser(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(UserProfile)
class AdminUserProfile(admin.ModelAdmin):
    list_display = ['id', 'user']
