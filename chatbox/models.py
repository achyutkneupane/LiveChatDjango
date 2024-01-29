from django.db import models
from drf_yasg import openapi


class Chatbox(models.Model):
    id = models.AutoField(primary_key=True)
    participants = models.ManyToManyField('the_auth.User')
    name = models.CharField(max_length=255, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @classmethod
    def schema(cls):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'participants': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER)
                ),
                'createdAt': openapi.Schema(type=openapi.TYPE_STRING),
                'updatedAt': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )

    class Meta:
        db_table = "chatboxes"
        ordering = ["-createdAt"]
        verbose_name = "Chatbox"
        verbose_name_plural = "Chatboxes"
        app_label = "chatbox"
