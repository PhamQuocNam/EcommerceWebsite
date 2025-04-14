from django.contrib import admin
from userauths.models import User, Profile
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email', 'Bio']
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','image','full_name','bio','phone','verified']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
