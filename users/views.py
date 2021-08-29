from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages #Flash request
from .forms import UserForm

def register(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Account created successfully!")
			return redirect('login')

	else:
		form = UserForm()
	return render(request, 'users/register.html', {'title': 'And so it begins...', 'form': form})

@login_required	
def account(request):
	return render(request, 'users/account.html', {'title' : 'Account'})

def login(request):
	return render(request, 'users/login.html', {'title' : 'Login'})

def logout(request):
	return render(request, 'users/logout.html', {'title': 'Logout'})	