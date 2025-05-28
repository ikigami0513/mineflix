from django.shortcuts import redirect
from django.http import HttpRequest


def superuser_required(view_func):
    def _wrapped_view(request: HttpRequest, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("index_view")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
