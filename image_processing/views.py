from io import BytesIO

import requests
from PIL import Image as PIL_Image
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView

from .models import Image


class ImageList(ListView):
    model = Image


class ImageDetail(DetailView):
    model = Image


class ImageCreate(CreateView):
    model = Image
    fields = ['file']

    def post(self, request, *args, **kwargs):
        if request.POST.get('url') and request.FILES.get('file'):
            return render(request, 'image_processing/image_form.html',
                          context={'error': f'Заполните только одно поле ({request.FILES["file"]})'})
        if not (request.POST.get('url') or request.FILES.get('file')):
            return render(request, 'image_processing/image_form.html',
                          context={'error': 'Заполните одно из полей'})
        if url := request.POST.get('url'):
            try:
                response = requests.get(url, stream=True)
            except:
                return render(request, 'image_processing/image_form.html',
                              context={'error': 'Введите верную ссылку'})
            response.raw.decode_content = True
            try:
                img = PIL_Image.open(response.raw)
            except Exception as e:
                return render(request, 'image_processing/image_form.html',
                              context={'error': f'Введите ссылку на изображение ({e})'})
            file_buffer = BytesIO()
            img.save(file_buffer, img.format)
            new_obj = Image()
            new_obj.file.save(url.split('/')[-1], ContentFile(file_buffer.getvalue()))
            new_obj.save()
            file_buffer.close()
            return redirect(new_obj)
        return super().post(request, *args, **kwargs)
