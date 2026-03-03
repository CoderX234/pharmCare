def user_role(request):
    role = None
    if request.user.is_authenticated:
        role = getattr(getattr(request.user, 'profile', None), 'role', None)
    return {'user_role': role}
