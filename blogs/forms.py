from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Blogs
import re
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields =['title', 'content', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def clean_title(self):
        '''
        Прописываем свою валидацию. Название не должно начинаться с цифры
        :return:
        '''
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', }))
