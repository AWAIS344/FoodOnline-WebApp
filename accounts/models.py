from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,first_name,last_name,email,username,password=None,):

        if not email and username:
            raise ValueError("User and Email Both are Required")
        
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    