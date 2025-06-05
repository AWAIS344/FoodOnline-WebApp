from .models import User,UserProfile
from django.db.models.signals import post_save,pre_save

from django.dispatch import receiver


@receiver(post_save,sender=User)
def post_save_userprofile_creation_signal(sender,instance,created,**kwargs):
    print(created)

    if created:
        UserProfile.objects.create(user=instance)
        print(f'user  with name {instance.username}  successfully Created')

    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)
            print("profile created dont exts earler")
        print("User Created Successfully")