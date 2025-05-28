from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class FavoritesUserList(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "users/favorite.html")
