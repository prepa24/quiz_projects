from .models import UserProfile

def user_profile(request):
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        return {'user_profile': profile}
    return {}
