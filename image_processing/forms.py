from django import forms

from .models import Image


class ImageCreateForm(forms.ModelForm):
    url = forms.URLField(label='Ссылка')

    class Meta:
        model = Image
        fields = ['url', 'file']