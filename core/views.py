"""Core views."""
import os

from django.shortcuts import render
# from django.views.generic import TemplateView, FormView
from django.views import View
import requests
from jseg import Jieba
from ckip import CkipSegmenter

from .forms import (
    SegmentationForm,
    ConcordanceForm,
)

jieba = Jieba()
ckip = CkipSegmenter()


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
                {'form': form, 'data': data})
        return render(request, self.template_name, {'form': form})


class SegmentationFormView(View):
    """Segmentation page."""

    template_name = 'segmentation.html'
    form_class = SegmentationForm

    initial = {
        'text': '中文斷詞真的很複雜◢▆▅▄▃ 崩╰(〒皿〒)╯潰 ▃▄▅▆◣',
        'algo': 'Jseg',
    }

    def get(self, request, *args, **kwargs):
        """GET method."""
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """POST method."""
        form = self.form_class(request.POST)
        if form.is_valid():
            from django.shortcuts import HttpResponse
            algo = form.cleaned_data['algo']
            text = form.cleaned_data['text']
            if algo == 'Jseg':
                output = ' '.join((
                    f'{char}|{pos}'
                    for (char, pos)
                    in jieba.seg(text, pos=True)
                ))
            elif algo == 'PyCCS':
                output = ckip.seg(text).raw
            elif algo == 'Segcom':
                output = 'NOT SUPPORTED YET!'
            return HttpResponse(output)
        return render(request, self.template_name)


def sentipol(request):
    """Sentipol page."""
    return render(request, 'sentipol.html')


def wordcloud(request):
    """Wordcloud page."""
    return render(request, 'wordcloud.html')
