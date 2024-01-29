from django.db import models


class Chatbox(models.Model):
    id = models.AutoField(primary_key=True)
    participants = models.ManyToManyField('the_auth.User')
    name = models.CharField(max_length=255, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "chatboxes"
        ordering = ["-createdAt"]
        verbose_name = "Chatbox"
        verbose_name_plural = "Chatboxes"
        app_label = "chatbox"
