from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок", help_text="Введите заголовок поста")
    content = models.TextField(verbose_name="Содержимое", help_text="Введите содержимое поста")
    preview = models.ImageField(upload_to="preview/", verbose_name="Превью", blank=True, null=True, help_text="Добавьте изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата и время изменения")
    is_public = models.BooleanField(default=True, verbose_name="Признак публикации", help_text="Укажите, доступен ли пост для просмотра")
    view_counter = models.IntegerField(default=0, help_text="Количество просмотров", verbose_name="Просмотров")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def send_congratulation_email(self):
        subject = f'Поздравляем! Пост "{self.title}" достиг 100 просмотров!'
        message = render_to_string('blog/email/congratulation.txt', {
            'post': self,
        })
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.MANAGER_EMAIL],
            fail_silently=False,
        )
