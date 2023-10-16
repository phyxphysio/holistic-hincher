from django.contrib import admin
from .models import MainCategory, SubCategory, Post
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, MembershipBenefits

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username","is_member"]



# Register your models here.
admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(Post)
admin.site.register(CustomUser)
admin.site.register(MembershipBenefits)





