from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

# Create your models here.

class AccountManager(BaseUserManager):

    def create_user(self, username,first_name, last_name, email, password=None):

        user = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using= self._db)
        return user
    
    def create_superuser(self, username, first_name, last_name, email, password):
        user = self.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            password = password,
        )

        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser  = True

        user.save(using = self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)


    #required
    data_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name']

    objects = AccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin


    def has_module_perms(self, add_label):
        return True










