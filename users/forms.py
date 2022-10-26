from logging import PlaceHolder
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'focus:outline-none bg-white w-4/5','placeholder':'demo@gmail.com'}))
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'focus:outline-none bg-white w-4/5','placeholder':'User123'}))
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'focus:outline-none bg-white w-4/5','placeholder':'First Name'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'focus:outline-none bg-white w-4/5','placeholder':'Last Name'}))
    password1 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'focus:outline-none bg-white w-4/5'}))
    password2 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'focus:outline-none bg-white w-4/5'}))

    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password1","password2")
    #Save data
    def save(self,commit=True):
        user = super(NewUserForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
