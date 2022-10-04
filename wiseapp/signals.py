from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from wiseapp.models import Profile, Code
# from .models import Code
# from .models import MultiReferral


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('i')
    if created:
        Profile.objects.create(user=instance)
        Code.objects.create(user=instance)
        # MultiReferral.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
