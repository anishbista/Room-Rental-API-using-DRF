from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from common.models import CommonInfo
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        name,
        address=None,
        mobile_no=None,
        profile_picture=None,
        password=None,
        password2=None,
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            mobile_no=mobile_no,
            address=address,
            profile_picture=profile_picture,
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


def validate_image_size(value):
    filesize = value.size

    if filesize > 1048576:
        raise ValidationError("The maximum file size that can be uploaded is 1 MB")


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=250, null=True)
    profile_picture = models.ImageField(
        upload_to="profile",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            validate_image_size,
        ],
    )
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
        return self.name

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
