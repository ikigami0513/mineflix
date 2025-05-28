from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import LoginForm


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = LoginForm()
        return render(request, "authentication/login.html", {
            "form": form
        })
    
    def post(self, request: HttpRequest) -> HttpResponse:    
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("index_view")
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe invalide.")

        return render(request, "authentication/login.html", {
            "form": form
        })
    

class LogoutView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect('login_view')
