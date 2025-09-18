from django.shortcuts import render
from django.http import HttpResponse


def show_form(request):
    '''Showe the form to the user'''
    template_name='formdata/form.html'

    return render(request, template_name)

def submit(request):
    '''Process form asubmission and generate result'''
    template_name = 'formdata/confirmation.html'
    print (request.POST)
    
    if request.POST:
        #extract from filed to variable
        name = request.POST['name']
        favcolor = request.POST['favorite_color']

        context = {
            'name': name,
            'favorite_color': favcolor,
        }

    return render(request, template_name=template_name, context=context)