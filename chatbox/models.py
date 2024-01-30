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


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey('the_auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    chatBox = models.ForeignKey(Chatbox, on_delete=models.CASCADE)
    replyTo = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    isForwarded = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    @classmethod
    def schema(cls):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'sender': openapi.Schema(type=openapi.TYPE_INTEGER),
                'content': openapi.Schema(type=openapi.TYPE_STRING),
                'chatBox': openapi.Schema(type=openapi.TYPE_INTEGER),
                'replyTo': openapi.Schema(type=openapi.TYPE_INTEGER),
                'isForwarded': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'createdAt': openapi.Schema(type=openapi.TYPE_STRING),
                'updatedAt': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )

    class Meta:
        db_table = "messages"
        ordering = ["-createdAt"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        app_label = "chatbox"
