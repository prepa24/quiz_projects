from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth import logout

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
            messages.success(request, "Pwofil ou mete ajou avèk siksè!")
            return redirect('profile')  # asire ou gen name='profile' nan urls.py

    else:
        profile_form = UserProfileForm(instance=profile)

    context = {
        'profile_form': profile_form,
        'profile': profile,  # OBLIGATWA pou image, bio, elatriye
    }
    return render(request, 'p_users/profile.html', context)

@login_required
def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, "Kont ou te siprime avèk siksè.")
    logout(request)
    return redirect("account_login")