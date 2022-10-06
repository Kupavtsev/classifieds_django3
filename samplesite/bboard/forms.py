# from django.forms import ModelForm, Form
from cProfile import label
from django import forms
from captcha.fields import CaptchaField

from .models import Bb, Rubric

class BbForm(forms.ModelForm):
    # captcha = CaptchaField(label='Введите текст с картинки',
    #                         error_messages={'invalid': 'Неправильный текст'})
    
    class Meta:
        model   = Bb
        fields  = ('title', 'content', 'price', 'kind', 'rubric')

class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово')
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика')


class CommentForm(forms.ModelForm):
    captcha = CaptchaField
    # class Meta:
    #     model = Comment