from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Message(models.Model):
    body = models.TextField(verbose_name="text")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="author")
    posted = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="posted")
    edited = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="edited")

    def __str__(self):
        return str(self.id)

    def get_create_url(self):
        return reverse('wall:add-comment', kwargs={'id': self.id, 'pk': 0})

    def get_update_url(self):
        return reverse('wall:edit-message', kwargs={'id': self.id})


class Comment(models.Model):
    body = models.CharField(max_length=255, verbose_name="comment")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="comments", verbose_name="message")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="author")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='parent')
    posted = models.DateTimeField(auto_now_add=True, verbose_name="posted")
    edited = models.DateTimeField(auto_now=True, verbose_name="edited")

    def __str__(self):
        return self.body

    def get_create_url(self):
        return reverse('wall:add-comment', kwargs={'id': self.message.id, 'pk': self.id})

    def get_update_url(self):
        return reverse('wall:edit-comment', kwargs={'id': self.id})