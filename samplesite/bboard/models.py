from django.db import models
from django.db.models.enums import Choices


class Bb(models.Model):

    class Kinds(models.TextChoices):
                    BUY = 'b', 'Куплю'
                    SELL = 's', 'Продам'
                    EXCHANGE = 'с', 'Обменяю'
                    RENT = 'r'
                    __empty__ = 'Выберите тип публикуемого объявления'

    kind        = models.CharField(
                            max_length=1,
                            choices=Kinds.choices,
                            default=Kinds.SELL
    )

    title       = models.CharField(
                            max_length=50,
                            verbose_name='Товар'
                            )
    content     = models.TextField(
                            null=True,                  # В необязательное поле можно занести пустое значение
                            blank=True,                 
                            verbose_name='Описание'
                            )
    
    price       = models.FloatField(
                            null=True,
                            blank=True,
                            verbose_name="Цена"
                            )
    published   = models.DateTimeField(
                            auto_now_add=True, 
                            db_index=True,              # Индекс по текущему
                            verbose_name="Опубликовано"
                            )
    changed   = models.DateTimeField(
                            auto_now=True, 
                            db_index=True,              # Индекс по текущему
                            verbose_name="Изменено"
                            )
    
    rubric      = models.ForeignKey(                    # Foreign Keys
                            'Rubric',
                            null=True,
                            on_delete=models.PROTECT,
                            verbose_name='Рубрика'
                            )


    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name        = 'Объявление'
        ordering            = ['-published']


class Rubric (models .Model) :
    name = models.CharField(
                    max_length=20,
                    db_index=True,
                    verbose_name='Название'
                    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name        = 'Рубрика'
        ordering            = ['name']