from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User #Model that will be effected
		fields = ['username', 'email', 'password1', 'password2']
		#Fields we want in the form, order specific.

