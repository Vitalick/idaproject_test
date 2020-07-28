import os
from io import BytesIO

import requests
from PIL import Image as PIL_Image
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView

from .models import Image


class ImageList(ListView):
    model = Image


class ImageDetail(UpdateView):
    model = Image
    fields = ['width', 'height']
    template_name = 'image_processing/image_detail.html'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        new_width = int(request.POST.get('width', '0'))
        new_height = int(request.POST.get('height', '0'))
        thumbnail = PIL_Image.open(self.object.file)
        format = thumbnail.format
        if not (new_width is 0 and new_height is 0):
            ratio = 1
            if new_width is 0:
                new_width = thumbnail.width / thumbnail.height * new_height
            elif new_height is 0:
                new_height = thumbnail.height / thumbnail.width * new_width
            else:
                width_ratio = new_width / thumbnail.width
                height_ratio = new_height / thumbnail.height
                if thumbnail.width * width_ratio > new_width or thumbnail.height * width_ratio > new_height:
                    ratio = height_ratio
                else:
                    ratio = width_ratio
            thumbnail = thumbnail.resize((int(thumbnail.width * ratio), int(thumbnail.height * ratio)), PIL_Image.ANTIALIAS)
        thumbnail_buffer = BytesIO()
        thumbnail.save(thumbnail_buffer, format)

        if self.object.thumbnail and os.path.isfile(self.object.thumbnail.path):
            os.remove(self.object.thumbnail.path)
        self.object.thumbnail.save(self.object.file.name.split('/')[-1], ContentFile(thumbnail_buffer.getvalue()))
        thumbnail_buffer.close()
        return redirect(self.object)


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
            if response.status_code != 200:
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
            new_obj.name = url.split('/')[-1]
            new_obj.save()
            file_buffer.close()
            return redirect(new_obj)
        return super().post(request, *args, **kwargs)
