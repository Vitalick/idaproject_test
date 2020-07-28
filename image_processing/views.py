from django.views.generic import ListView, DetailView, CreateView

# Create your views here.
from .models import Image


class ImageList(ListView):
    model = Image


class ImageDetail(DetailView):
    model = Image


class ImageCreate(CreateView):
    model = Image
    fields = ['file', ]
