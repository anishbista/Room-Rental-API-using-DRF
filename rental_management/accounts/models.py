from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from common.models import CommonInfo


class UserManager(BaseUserManager):
    def create_user(
        self, email, name, address, mobile_no=None, password=None, password2=None
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            mobile_no=mobile_no,
            address=address,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        name,
        password=None,
    ):

        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=10)
    address = models.CharField(max_length=250)
    profile_picture = models.ImageField(upload_to="profile", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
    ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# class CustomUser(AbstractUser):
#     mobile_no = models.CharField(max_length=10)
#     address = models.CharField(max_length=250)
#     profile_picture = models.ImageField(upload_to="profile", blank=True, null=True)


class OTP(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    otp = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"
