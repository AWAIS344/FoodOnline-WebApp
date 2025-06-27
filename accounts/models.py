from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,first_name,last_name,email,username,password=None):

        if not email or not username:
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
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    objects=UserManager()

    VENDOR=1
    CUSTOMER=2

    role_choices=[
        (VENDOR,"Restaurent"),
        (CUSTOMER,"Customer"),
    ]

    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100 , unique=True)
    username=models.CharField(max_length=50, unique=True)
    phone_number=models.CharField(max_length=12, unique=True,null=True)
    role=models.PositiveSmallIntegerField(choices=role_choices, blank=True , null= True)

    #RequiredFields
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    modifies=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
 
    USERNAME_FIELD='email'  #batata hai ke login ke liye konsa field use hoga

    REQUIRED_FIELDS=["first_name","last_name","username"]

    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True
    
    def user_role(self):

        if self.role == 1:
            user_role="Vendor"
        
        elif self.role == 2: 
            user_role="Customer"
        return user_role
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


    def __str__(self):
        return self.username
    

class UserProfile(models.Model):
    user = models.OneToOneField(User,blank=True,null=True,on_delete=models.CASCADE)
    profile_image=models.ImageField(upload_to="user/profile_img")
    cover_image=models.ImageField(upload_to="user/cover_img")
    address=models.CharField(max_length=250,blank=True,null=True)

    country=models.CharField(max_length=30,blank=True,null=True)
    state=models.CharField(max_length=30,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    pincode=models.CharField(max_length=6,blank=True,null=True)
    logitude=models.CharField(max_length=20,blank=True,null=True)
    latitude=models.CharField(max_length=20,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    

    