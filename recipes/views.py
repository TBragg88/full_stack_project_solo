from django.shortcuts import render

# Create your views here.

def home_view(request):
    """
    This function handles requests to the home page
    - request: Django automatically passes this - contains info about the user's request
    - render(): Takes the request + template name + data, returns HTML response
    """
    return render(request, 'recipes/home.html')