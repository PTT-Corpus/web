"""Core views."""
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.views import View

from .forms import ConcordanceForm


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


class ConcordanceFormView(View):
    """Concordance page."""
    template_name = 'concordance.html'
    form_class = ConcordanceForm

    initial = {
        'word': '帥哥',
        'page': 0,
        'post_type': 0,
        'order': 'desc',
        'sort': 'published',
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})




def segmentation(request):
    """Segmentation page."""
    return render(request, 'segmentation.html')


def sentipol(request):
    """Sentipol page."""
    return render(request, 'sentipol.html')


def wordcloud(request):
    """Wordcloud page."""
    return render(request, 'wordcloud.html')
