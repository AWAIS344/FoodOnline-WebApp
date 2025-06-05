from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,first_name,last_name,email,username,password=None):

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
    
    def create_superuser(self,first_name,last_name,email,username,password=None):
        user=self.create_user(

            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        return user


class User(AbstractBaseUser):

    objects=UserManager()

    RESTAURENT=1
    CUSTOMER=2

    role_choices=[
        (RESTAURENT,"Restaurent"),
        (CUSTOMER,"Customer"),
    ]

    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100 , unique=True)
    username=models.CharField(max_length=50, unique=True)
    phone_number=models.CharField(max_length=12, unique=True,null=True)
    role=models.PositiveSmallIntegerField(choices=role_choices)

    #RequiredFields
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    modifies=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_actve=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD='email'

    REQUIRED_FIELDS=["first_name","last_name","username"]

    def has_perm(self,perm , obj=None):
        return self.is_admin
    
    def has_module_perm(self,app_label):
        return True


    def __str__(self):
        return self.username
    


    