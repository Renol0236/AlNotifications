from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile, Notifications

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(widget=forms.PasswordInput)

class UserCreateForm(UserCreationForm):

    email = forms.EmailField()
    bio = forms.CharField(max_length=500)
    profile_picture = forms.ImageField(required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['password2', 'username']:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'profile_picture']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'phone', 'full_name', 'address']