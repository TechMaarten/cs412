from django.shortcuts import render
import random

# make a global list
quotes = [
    "I'm ready! I'm ready! I'm ready!",
    "Can I be excused for the rest of my life?",
    "I'm ugly and I'm proud!"
]

images = [
    "https://i.scdn.co/image/ab67616100005174877d4c061d08c040974224be",
    "https://static.wikia.nocookie.net/viacom4633/images/4/47/Spongebob.png/revision/latest/thumbnail/width/360/height/360?cb=20241216025934",
    "https://cloudfront-us-east-1.images.arcpublishing.com/opb/UODRDCE3KTLWUWUHHRETSAXL7U.jpg",
]

# views
def quote(request):
    context = {
        'quote': random.choice(quotes),
        'image': random.choice(images)
    }
    return render(request, 'quote.html', context)

def show_all(request):
    context = {
        'quotes': quotes,
        'images': images
    }
    return render(request, 'show_all.html', context)

def about(request):
    return render(request, 'about.html')

