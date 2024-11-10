from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if profile_form.is_valid():
            profile_form.save()
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.save()
            return redirect('profile')  # Change 'profile' to the name of the URL that displays the profile

    else:
        profile_form = UserProfileForm(instance=profile)

    context = {
        'profile_form': profile_form,
        'user': request.user,
    }
    return render(request, 'p_users/profile.html', context)
