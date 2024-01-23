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
