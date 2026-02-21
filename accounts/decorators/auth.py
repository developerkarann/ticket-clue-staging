from django.shortcuts import render, get_object_or_404, redirect

def user_not_logged_in(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = 'home'  # Default redirect URL

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator