from django.core.exceptions import ValidationError
from django.db import models
# from django.contrib.auth.models import User
from django.core import validators
from django.contrib.auth.models import User

#           ========================================= 
#           ---===Personal validators in Models===---
#           ========================================= 
def get_min_length():        # It works, but it doesn't show any messages!!!
    min_length = 3           # But before testapp, it works correctly
    return min_length

def validate_even(val):     # It works, but it doesn't show any messages!!!
    pass
    # if val % 2 != 0:
        # raise ValidationError(f'Число {val} нечетное', code='odd')


#           ========================================= 
#           ---===      Main class of ads      ===---
#           ========================================= 
class Bb(models.Model):

    class Kinds(models.TextChoices):
                    BUY = 'b', 'Куплю'
                    SELL = 's', 'Продам'
                    EXCHANGE = 'с', 'Обменяю'
                    RENT = 'r'
                    __empty__ = 'Выберите тип публикуемого объявления'

    STATUS = (
        ('Куплю', 'Куплю'), ('Продам', 'Продам'), ('Обменяю', 'Обменяю')
    )

    title = models.CharField(
        max_length=50, verbose_name='Товар', 
        validators=[validators.MinLengthValidator(get_min_length)],
        # error_messages={'invalid': 'Минимальная длинна 5, максимальная 50'}   # it doesn't display any
                                    )
    # В необязательное поле можно занести пустое значение: null/blank = True
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name="Цена", validators=[validate_even])
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")
    rubric = models.ForeignKey(
        'Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика',
        limit_choices_to={'show': True} #  limit_choices_to в форме работает но отображается на сайте
        )
    changed = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Изменено")
    kind = models.CharField(max_length=7, choices=STATUS, default=STATUS[1])
    # kind = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.SELL)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='User')
    # author =  models.CharField(max_length=50, null=True, blank=True, verbose_name='Автор', default=None)      # am I need this to work with admin as user?
                                    

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name        = 'Объявление'
        ordering            = ['-published']
        # order_with_respect_to = 'rubric'  # there is no attriute for this parametr
        
        unique_together     = ('title', 'price')    # Ограничение на уже имеющуюся комбинацию в БД
        # constraints у меня не работает
        # constraints          = (
        #     models.CheckConstraint(check=models.Q(price__gte=0) & models.Q(
        #         price__lte=10000),
        #         name='%(app_label)s_%(class)s_price_constraint'),
        # )
    def title_and_price(self):
        if self.price:
            return f'{self.title}: {self.price} rub.'
        else:
            return self.title


#           ========================================= 

class Rubric(models.Model) :

    def get_absolute_url(self):
        # return "/bboard/%s" % self.pk
        return f'/bboard/{self.pk}'

    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')
    show = models.BooleanField(default=True)    # Its doesnt work!!!
    # order = models.SmallIntegerField(default=0, db_index=True, blank=True, null=True)   # makemigration: no such column

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name        = 'Рубрика'
        ordering            = ['name']