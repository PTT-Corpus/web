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
from .data import boards

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
        'word': '台灣',
        'post_type': 0,
        'order': 'desc',
        'sort': 'published',
        'pos': False,
    }

    def get(self, request, *args, **kwargs):
        """GET method."""
        form = self.form_class(initial=self.initial)
        return render(
            request,
            self.template_name,
            {'form': form, 'boards': boards}
        )

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
                request,
                'concordance_result.html',
                {
                    'form': form,
                    'data': data,
                    'query': request.POST
                }
            )

        return render(request, self.template_name, {'form': form})


class SegmentationFormView(View):
    """Segmentation page."""

    template_name = 'segmentation.html'
    form_class = SegmentationForm

    initial = {
        'text': '人文學群的Python程式設計入門。\
人文社會學群學習者不能安於對於現有程式語法的熟悉和背誦，\
或被規訓成為現有虛擬世界的消費者。\n\
在人文社會精神下培養計算思維，才能讓虛擬\
世界變複數型，開啟人機互動的更多可能。',
        'algo': 'Segcom',
    }

    def get(self, request, *args, **kwargs):
        """GET method."""
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """POST method."""
        form = self.form_class(request.POST)
        if form.is_valid():
            algo = form.cleaned_data['algo']
            text = form.cleaned_data['text']
            if algo == 'Jseg':
                output = ' '.join((
                    f'{char}|<span class="pos">{pos}</span>'
                    for (char, pos)
                    in jieba.seg(text, pos=True)
                ))
            elif algo == 'PyCCS':
                res = ckip.seg(text)
                output = ' '.join((f'{char}|<span class="pos">{pos}</span>'
                                   for (char, pos)
                                   in zip(res.tok, res.pos)))
            elif algo == 'Segcom':
                output = self._segcom(text)
            return render(request, 'segmentation_result.html',
                          {'algo': algo, 'output': output})
        return render(request, self.template_name)

    def _segcom(self, txt):
        jres = jieba.seg(txt)
        cres = ckip.seg(txt).tok
        if (
            len(''.join(jres).replace(' ', '').replace('\n', '')) !=
            len(''.join(cres).replace(' ', '').replace('\n', ''))
        ):
            raise Exception(
                'Unequal length of results, fail to compare'
            )
        source = ''.join(jres)
        cnt_j, cnt_c = 0, 0
        idxcon_j, idxcon_c = [], []
        for word in jres:
            idx = ''
            for char in word:
                idx += f'_{cnt_j}'
                cnt_j += 1
            idxcon_j.append(idx)
        for word in cres:
            idx = ''
            for char in word:
                idx += f'_{cnt_c}'
                cnt_c += 1
            idxcon_c.append(idx)

        ovlps = set(idxcon_j) & set(idxcon_c)
        output_j, output_c = '', ''
        for i in idxcon_j:
            idxs = [int(j) for j in i.split('_') if j != '']
            recv = ''.join([source[idx] for idx in idxs])
            if i in ovlps:
                output_j += recv
            else:
                output_j += '<span class="diff">%s</span>' % recv
            output_j += ' '
        for i in idxcon_c:
            idxs = [int(j) for j in i.split('_') if j != '']
            recv = ''.join([source[idx] for idx in idxs])
            if i in ovlps:
                output_c += recv
            else:
                output_c += '<span class="diff">%s</span>' % recv
            output_c += ' '
        return (output_j, output_c)


def sentipol(request):
    """Sentipol page."""
    return render(request, 'sentipol.html')


def wordcloud(request):
    """Wordcloud page."""
    return render(request, 'wordcloud.html')
