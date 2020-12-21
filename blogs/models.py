from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Blogs(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок поста')
    content = models.TextField(max_length=1000, verbose_name='Текст')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, )
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date_created']


class Subscribers(models.Model):
    user_from = models.ForeignKey(User, related_name='user_to', on_delete=models.CASCADE, )
    user_to = models.ForeignKey(User, related_name='user_from', on_delete=models.CASCADE, )


# User.add_to_class('following',
#                   models.ManyToManyField('self', through=Subscribers, related_name='followers', symmetrical=False))
