from django.shortcuts import render, redirect
from django.contrib import messages
from core import forms


def register(request):
    if request.user.is_authenticated:
        return redirect(to="home")

    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, message="Registration was successfull, Please login to continue")
            return redirect("login")
    else:
        form = forms.RegistrationForm()

    return render(request, "core/signup.html", {'form': form})
