from django.contrib.auth.models import BaseUserManager

class CustomUserManager():
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not password:
            raise ValueError("The Password field must be set")
        
        email = self.normalize_email(email)
        user = self.model(
            username=username.strip(), 
            email=email,
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        return self.create_user(username, email, password, **extra_fields)
