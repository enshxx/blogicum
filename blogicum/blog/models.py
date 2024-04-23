from core.models import PublishedModel
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(PublishedModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True,
                            verbose_name='Идентификатор',
                            help_text='Идентификатор страницы для URL;'
                                      ' разрешены символы латиницы, цифры,'
                                      ' дефис и подчёркивание.')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(PublishedModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Post(PublishedModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации',
                                    help_text='Если установить дату и время в '
                                    'будущем — можно делать отложенные'
                                    ' публикации.')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор публикации'
                               )
    location = models.ForeignKey(Location,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name='Местоположение'
                                 )
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name='Категория',
                                 related_name='posts'
                                 )
    image = models.ImageField('Фото', upload_to='post_images', blank=True)
    comment_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, **kwargs):
        super().save(**kwargs)
        self.post.comment_count = Comment.objects.filter(
            post=self.post).count()

    class Meta:
        ordering = ('created_at',)
