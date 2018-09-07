"""Core views."""
import os

from django.shortcuts import render
# from django.views.generic import TemplateView, FormView
from django.views import View
import requests

from .forms import ConcordanceForm


def index(request):
    """Index page."""
    return render(request, 'index.html')


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
        'word': '好雷',
        'boards': 'movie',
        'post_type': 0,
        'order': 'desc',
        'sort': 'published',
    }

    def get(self, request, *args, **kwargs):
        """GET method."""
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """POST method."""
        form = self.form_class(request.POST)
        if form.is_valid():
            resp = requests.get(
                os.environ['PTT_ENGINE'] + 'query',
                {k: v for k, v in form.cleaned_data.items() if v},
            )
            data = resp.json()
            return render(
                request, 'concordance_result.html',
                {'data': data})
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
