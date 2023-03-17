from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, firstname, lastname, password, active=True, staff=False, admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            firstname=firstname,
            lastname=lastname
        )
        user.set_password(password)  # change user password
        user.staff = staff
        user.admin = admin
        user.active = active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, firstname, lastname, password):
        user = self.create_user(
            email,
            username,
            firstname,
            lastname,
            password,
            staff=True,
            admin=True,
            active=True

        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=100, blank=False, unique=True)
    username = models.CharField(verbose_name='username', max_length=30, unique=True)
    firstname = models.CharField(verbose_name='firstname', max_length=30, blank=True)
    lastname = models.CharField(verbose_name='lastname', max_length=30, blank=True)

    active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email'  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['username', 'firstname', 'lastname']  # ['full_name'] #python manage.py createsuperuser

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_firstname(self):
        if self.firstname:
            return self.firstname
        return self.email

    def get_lastname(self):
        if self.lastname:
            return self.lastname
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
