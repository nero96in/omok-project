from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User

from .form import SignupForm

# User = get_user_model()


# class UserAdmin(BaseUserAdmin):
#     fieldsets = BaseUserAdmin.fieldsets + (
#         ('추가 정보', {'fields': ('email','nickname','win', 'draw','lose')}),
#     )
#     add_form = SignupForm

admin.site.register(User)