from django import forms
from .models import *

from django.contrib.auth.models import User

class SelectFileForm(forms.ModelForm):
    '''
        Form with the info of the file that contains the code
    '''
    class Meta:
            model = AppCodeFile # Selected File 
            fields = ('My_file',)
            
class UpdateUserForm(forms.ModelForm):
    '''
        Form with the info of the user
    '''
    # Obligatory data
    
    class Meta:
            model = User
            fields = ('first_name','last_name','email',)
            
class UserProfileForm(forms.ModelForm):
    '''
        Form with additional info
    '''
    class Meta:
        model = UserProfile
        fields = ('appinventorLogin',)
        
        
class CreateUserForm(forms.Form):
    '''
        Form with the info of the user
    '''
    username = forms.CharField(max_length=30)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email=forms.EmailField()
    password1=forms.CharField(max_length=30,widget=forms.PasswordInput()) 
    password2=forms.CharField(max_length=30,widget=forms.PasswordInput())
    appinventorLogin = forms.CharField()
        