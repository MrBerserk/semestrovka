from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Game(BaseModel):
    user = models.ForeignKey(User, verbose_name='пользователь', related_name='user_games', on_delete=models.CASCADE)
    title = models.CharField(max_length=80, verbose_name='название игры')
    slug = models.SlugField(max_length=80, verbose_name='слаг', unique_for_date='created_at')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(null=True, blank=True, upload_to='games_images', verbose_name='скрин из игры')
    price = models.IntegerField(null=True, blank=True, verbose_name='цена',
                                validators=[MinValueValidator(1), MaxValueValidator(5000)])

    class Meta:
        verbose_name_plural = 'Игры'
        verbose_name = 'Игра'

    def __str__(self):
        return self.title


class Favourite(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователь', related_name='user_favourite', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, verbose_name='игра', related_name='game_favourite', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Список желаемого'
        verbose_name = 'Список желаемого'


class Comment(BaseModel):
    game = models.ForeignKey(Game, verbose_name='игра', related_name='game_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='пользователь', related_name='user_comments', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='текст комментарий')

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text


class UserInfo(BaseModel):
    user = models.ForeignKey(User, related_name='user_info', verbose_name='пользователь', on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=40, verbose_name='имя')
    about = models.TextField(null=True, blank=True, max_length=200, verbose_name='информация о себе')

    class Meta:
        verbose_name_plural = 'Информация о пользователях'
        verbose_name = 'Информация о пользователе'

    def __str__(self):
        return self.name


class Basket(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователь', related_name='user_basket', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, verbose_name='игра_в_корзине', related_name='game_basket', on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modificated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Корзины пользователей'
        verbose_name = 'Корзина пользователя'

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.game.title}'

    def sum(self):
        return self.product.price
