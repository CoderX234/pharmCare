from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def role_required(allowed_roles=None, redirect_to='login'):
    if allowed_roles is None:
        allowed_roles = []

    def check(user):
        if not user.is_authenticated:
            return False
        # Expect a Profile with role attribute
        role = getattr(getattr(user, 'profile', None), 'role', None)
        return role in allowed_roles or user.is_superuser

    def decorator(view_func):
        return user_passes_test(check, login_url=redirect_to)(view_func)

    return decorator
