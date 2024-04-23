from django.db import models


class PublishedModel(models.Model):
    is_published = models.BooleanField(default=True,
                                       verbose_name="Опубликовать",
                                       help_text='Снимите галочку,'
                                                 ' чтобы скрыть публикацию.')
    created_at = models.DateTimeField(verbose_name="Добавлено",
                                      auto_now_add=True)

    class Meta:
        abstract = True
