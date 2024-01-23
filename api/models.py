from django.db import models


class User(models.Model):
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50, blank=True)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        if not self.middleName:
            return self.firstName + " " + self.lastName
        return self.firstName + " " + self.middleName + " " + self.lastName

    class Meta:
        db_table = "users"
        ordering = ["-createdAt"]
        verbose_name = "User"
        verbose_name_plural = "Users"


class Login(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userAgent = models.CharField(max_length=50)
    ipAddress = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " logged in at " + str(self.createdAt)

    class Meta:
        db_table = "logins"
        ordering = ["-createdAt"]
        verbose_name = "Login"
        verbose_name_plural = "Logins"
