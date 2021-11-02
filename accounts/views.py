from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UsersLoginForm, UsersRegisterForm

def login_view(request):
	form = UsersLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username = username, password = password)
		login(request, user)
		return redirect("/")
	return render(request, "accounts/form.html", {
		"form" : form,
		"title" : "Login",
	})


def register_view(request):
    pass

from django.contrib.auth import logout
from django.http import HttpResponseRedirect

def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/")