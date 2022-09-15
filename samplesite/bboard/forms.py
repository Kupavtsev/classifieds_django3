# from django.forms import ModelForm, Form
from django import forms
from .models        import Bb, Rubric

class BbForm(forms.ModelForm):
    class Meta:
        model   = Bb
        fields  = ('title', 'content', 'price', 'kind', 'rubric')

class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово')
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика')
