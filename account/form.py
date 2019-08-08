from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField




class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ['username', 'password']
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ['username','password1', 'password2','nickname','email']
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'nickname',
            'email',
            
            
            
            
        )
        # widgets = {
        #     'username': forms.TextInput(
        #         attrs={
        #             'class': 'form-control',
        #         }
        #     ),
        
           
        # }




