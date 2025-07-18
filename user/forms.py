from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User, Permission, Group
from events.forms import StyledFormMixing
from django import forms
import re

class CustomRegisterForm(StyledFormMixing, forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    confirm_password = forms.CharField(widget= forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []

        if len(password)<8:
            errors.append('Password must be at least 8 characters')

        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$'

        if not re.fullmatch(pattern, password):
            errors.append(
                'Password must include at least one uppercase letter, one lowercase letter, '
                'one number, and one special character.'
            )
        
        if errors:
            raise forms.ValidationError(errors)
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password do not match. Try again')
        
        return cleaned_data
    
    def email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email = email).exists()

        if email_exists:
            raise forms.ValidationError('This email already exist, use new one')
        
        return email

class LoginForm(StyledFormMixing, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AssignedRoleForm(StyledFormMixing,forms.Form):
    role = forms.ModelChoiceField(
        queryset = Group.objects.all(),
        empty_label= "Select a role",
        label="Role"
    )

class CreateGroupForm(StyledFormMixing, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = 'Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name','permissions']