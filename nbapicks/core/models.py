from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("You must enter a username")
        
        if not email:
            raise ValueError("You must enter an email")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Team(models.Model):
    name = models.CharField(max_length=50)
    logo = models.FileField(upload_to="static/logos")

    def __str__(self):
        return self.name


class Game(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="home_team")
    home_team_score = models.BigIntegerField(null=True)
    away_team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="away_team")
    away_team_score = models.BigIntegerField(null=True)
    date = models.DateField()
    winner = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="winner", null=True)



class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True)
    successful_picks = models.IntegerField(default=0)
    total_picks = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Pick(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    team_picked = models.ForeignKey(Team, on_delete=models.PROTECT)
    successful_pick = models.BooleanField(null=True)


class Contact(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    title = models.CharField(max_length=50)
    message = models.TextField(max_length=2000)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.email