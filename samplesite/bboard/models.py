from django.db import models
from django.contrib.auth.models import User
from django.core import validators

def get_min_length():
    min_length = 5
    return min_length

class Bb(models.Model):

    class Kinds(models.TextChoices):
                    BUY = 'b', 'Куплю'
                    SELL = 's', 'Продам'
                    EXCHANGE = 'с', 'Обменяю'
                    RENT = 'r'
                    __empty__ = 'Выберите тип публикуемого объявления'

    kind        = models.CharField(max_length=1,choices=Kinds.choices,default=Kinds.SELL)
    title       = models.CharField(max_length=50, verbose_name='Товар', 
                                    validators=[validators.MinLengthValidator(get_min_length)])
    # В необязательное поле можно занести пустое значение: null/blank = True
    content     = models.TextField(null=True, blank=True, verbose_name='Описание')
    price       = models.FloatField(null=True, blank=True, verbose_name="Цена")
    published   = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")
    changed     = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Изменено")
    rubric      = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика',
                                     limit_choices_to={'show': True})
                                    #  limit_choices_to в форме работает но отображается на сайте


    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name        = 'Объявление'
        ordering            = ['-published']
        
        unique_together     = ('title', 'price')    # Ограничение на уже имеющуюся комбинацию в БД
        # constraints у меня не работает
        # constraints          = (
        #     models.CheckConstraint(check=models.Q(price__gte=0) & models.Q(
        #         price__lte=10000),
        #         name='%(app_label)s_%(class)s_price_constraint'),
        # )


class Rubric(models.Model) :

    def get_absolute_url(self):
        # return "/bboard/%s" % self.pk
        return f'/bboard/{self.pk}'

    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')
    some = models.CharField(max_length=4, verbose_name='Some test') # ??????
    show = models.BooleanField(default=True)    # Не дает возможность выбрать рубрику False

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name        = 'Рубрика'
        ordering            = ['name']



class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Активированные'
        verbose_name        = 'Активированный'
        ordering            = ['is_activated']