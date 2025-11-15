"""Maarten Lopes, lopesmaa@bu.edu"""
"""dadjokes/api_views.py"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer

@api_view(['GET'])
def api_random(request):
    joke = Joke.objects.order_by('?').first()
    return Response(JokeSerializer(joke).data)

@api_view(['GET'])
def api_random_picture(request):
    pic = Picture.objects.order_by('?').first()
    return Response(PictureSerializer(pic).data)

@api_view(['GET', 'POST'])
def api_jokes(request):
    if request.method == 'GET':
        jokes = Joke.objects.all().order_by('-created_at')
        return Response(JokeSerializer(jokes, many=True).data)

    if request.method == 'POST':
        serializer = JokeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_joke_detail(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    return Response(JokeSerializer(joke).data)

@api_view(['GET'])
def api_pictures(request):
    pics = Picture.objects.all().order_by('-created_at')
    return Response(PictureSerializer(pics, many=True).data)

@api_view(['GET'])
def api_picture_detail(request, pk):
    pic = get_object_or_404(Picture, pk=pk)
    return Response(PictureSerializer(pic).data)
