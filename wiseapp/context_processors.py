from .models import Profile


# used to pass profile into base html
def message_processor(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        bot_status = profile.run_profile_button_flag
    else:
        profile = None
        bot_status = None
    return {
        'profile': profile,
        'bot_status':  bot_status
    }