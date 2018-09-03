"""Core views."""
from django.shortcuts import render


def index(request):
    """Index page."""
    return render(request, 'index.html')


def home(request):
    """Home."""
    return render(request, 'core/home.html')


def apidoc(request):
    """Documentation page for API."""
    return render(request, 'apidoc.html')


def collocation(request):
    """Collocation page."""
    return render(request, 'collocation.html')


def concordance(request):
    """Concordance page."""
    return render(request, 'concordance.html')


def segmentation(request):
    """Segmentation page."""
    return render(request, 'segmentation.html')


def sentipol(request):
    """Sentipol page."""
    return render(request, 'sentipol.html')


def wordcloud(request):
    """Wordcloud page."""
    return render(request, 'wordcloud.html')
