from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# Regular imports
from random import randint
from uuid import uuid4
from datetime import datetime as dt

# Create your models here.
class AuthManager(BaseUserManager):
    # @staticmethod
    def describe_manager(self):
        print(self.db, self.model )


    def create_user(self, first_name="", last_name="", email_address=None, is_active=True, is_admin=False, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email_address:
            raise ValueError('Users must have an email address')
        # if not email_address:
        #     raise ValueError('Users must have an email address')
        # if not email_address:
        #     raise ValueError('Users must have an email address')

        user_name = first_name[0] + last_name + str(randint(1000, 1000000))
        #TODO: Fix the username bug. add condition to make it unique.

        user = self.model(
            user_id=uuid4(),
            first_name=first_name,
            last_name=last_name,
            email_address=self.normalize_email(email_address),
            is_active=is_active,
            is_admin=is_admin,
            user_name=user_name,
            last_logged_in=dt.now()
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name=None, first_name="", last_name="", email_address=None, is_active=True, is_admin=False, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.model(
            user_id=uuid4(),
            first_name=first_name,
            last_name=last_name,
            email_address=self.normalize_email(email_address),
            is_active=is_active,
            user_name=user_name,
            last_logged_in=dt.now()
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class AuthEmployeeRegisterModel(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=False, null=False, verbose_name="First name", help_text="First name of the employee")
    last_name = models.CharField(max_length=100, blank=False, null=False, verbose_name="Last name", help_text="Last name of the employee")
    email_address = models.EmailField(max_length=250, blank=False, null=False, verbose_name="Email address", help_text="Email address of the employee")
    user_name = models.CharField(max_length=100, blank=False, null=False, unique=True, verbose_name="Username", help_text="Username of employee")
    password = models.CharField(max_length=100, blank=False, null=False, verbose_name="Password", help_text="Password of the account", validators=[MinLengthValidator(8)])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_logged_in = models.DateField()

    USERNAME_FIELD = 'user_name'

    objects = AuthManager()

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

        
    