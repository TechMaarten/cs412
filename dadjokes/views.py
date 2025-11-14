from django.shortcuts import render, get_object_or_404
from .models import Joke, Picture

def index(request):
    joke = Joke.objects.order_by('?').first()
    pic = Picture.objects.order_by('?').first()
    return render(request, 'dadjokes/index.html', {'joke': joke, 'pic': pic})

def random_view(request):
    return index(request)

def jokes_list(request):
    jokes = Joke.objects.all()
    return render(request, 'dadjokes/jokes_list.html', {'jokes': jokes})

def joke_detail(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    return render(request, 'dadjokes/joke_detail.html', {'joke': joke})

def pictures_list(request):
    pics = Picture.objects.all()
    return render(request, 'dadjokes/pictures_list.html', {'pics': pics})

def picture_detail(request, pk):
    pic = get_object_or_404(Picture, pk=pk)
    return render(request, 'dadjokes/picture_detail.html', {'pic': pic})
