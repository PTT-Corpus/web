"""Core views."""
import os
import urllib.parse

from django.shortcuts import render
from django.views import View
import requests
from jseg import Jieba
from ckip import CkipSegmenter

from .forms import (
    SegmentationForm,
    ConcordanceForm,
)
from .data import boards
from .concordance import get_concordance

from .blacklab_api import *

API_URI = os.environ['PTT_BACKEND_URL']
PUBLIC_API_URI = os.environ['PTT_BACKEND_PUBLIC_URL']

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
        'post_type': 3,
        'cql_enable': False,
         # 'order': 'desc',
         # 'sort': 'published',
        'pos': False,
        'window_size': 10,
        'size': 50,
    }

    def get(self, request, *args, **kwargs):
        """GET method."""
        form = self.form_class(initial=self.initial)

        print(boards)
        return render(
            request,
            self.template_name,
            {'form': form}
            # {'form': form, 'boards': boards}
        )

    def post(self, request, *args, **kwargs):
        """POST method."""
        data = dict()

        form = self.form_class(request.POST)
        if form.is_valid():
            # 原本是要去 Elasticsearch 問
            # resp = requests.get(
            #     os.environ['PTT_ENGINE'] + 'query',
            #     {k: v for k, v in form.cleaned_data.items() if v},
            # )

            print(form.cleaned_data)
            show_pos = request.POST.get('pos', False)
            
            # size 指的是一頁要顯示幾筆
            data['size'] = form.cleaned_data['size']

            if form.cleaned_data['page'] is None:
                data['page'] = 0
            else:
                data['page'] = int(form.cleaned_data['page'])

            data['page_times_size'] = data['size'] * data['page']

            # 根據 size 和 page 計算出這一頁要顯示哪幾個concordance line
            start_index = data['size'] * data['page']
            # end_index = data['size'] * (data['page'] + 1)

            result = blacklab_get_concordance(
                query=form.cleaned_data['word'],
                board=form.cleaned_data['boards'],
                text_type=form.cleaned_data['post_type'],
                show_pos=show_pos,
                cql_enable=form.cleaned_data['cql_enable'],
                window_size=form.cleaned_data['window_size'],
                start_year=form.cleaned_data['start'],
                end_year=form.cleaned_data['end'],
                hits_per_page=form.cleaned_data['size'],
                start_index=start_index,
            )

            # 表示出錯
            if type(result) is tuple:
                error_code = result[0]
                error_log = result[1]

                return render(request, self.template_name, {'form': form, 'error': error_log})

            # 總共有幾個concordance line
            data['total'] = result['totalHits']

            # keys_of_result_dict = list(result.keys())
            # target_concordance_key = keys_of_result_dict[start_index:end_index]

            data['concordance'] = list()

            # for i in target_concordance_key:
                # df = result[i]
            # if show_pos:
            #     for _, df in result.items():    
            #         data['concordance'].append({
            #             'left': ' '.join(df.loc[df['offset'] < 0, ['word', 'pos']].apply(lambda x: '##'.join(x), axis=1)),
            #             'key': ' '.join(df.loc[df['offset'] == 0, ['word', 'pos']].apply(lambda x: '##'.join(x), axis=1),),
            #             'right': ' '.join(df.loc[df['offset'] > 0, ['word', 'pos']].apply(lambda x: '##'.join(x), axis=1),)
            #         })
            # else:
            #     for _, df in result.items():    
            #         data['concordance'].append({
            #             'left': ' '.join(df.loc[df['offset'] < 0, 'word'].tolist()),
            #             'key': ' '.join(df.loc[df['offset'] == 0, 'word'].tolist()),
            #             'right': ' '.join(df.loc[df['offset'] > 0, 'word'].tolist())
            #         })


            if show_pos:
                for hit in result['hits']:
                    data['concordance'].append({
                        'left': ' '.join([f"{hit['left']['word'][i]}##{hit['left']['pos'][i]}" for i, _ in enumerate(hit['left']['word'])]),
                        'key': ' '.join([f"{hit['match']['word'][i]}##{hit['match']['pos'][i]}" for i, _ in enumerate(hit['match']['word'])]),
                        'right': ' '.join([f"{hit['right']['word'][i]}##{hit['right']['pos'][i]}" for i, _ in enumerate(hit['right']['word'])]),

                    })
            else:
                for hit in result['hits']:
                    data['concordance'].append({
                        'left': ' '.join(hit['left']['word']),
                        'key': ' '.join(hit['match']['word']),
                        'right': ' '.join(hit['right']['word']),

                    })

            # print(data['concordance'])
            param = {
                "outputformat": "csv",
                "indexname": "indexes",
                "patt": result['patt'],
                "filter": result['filter']
            }

            encoded_param = urllib.parse.urlencode(param)
            link_for_output = f"{PUBLIC_API_URI}/hits-csv?{encoded_param}"
            # link_for_output = urllib.parse.quote(link_for_output, safe=':/&?="')

            return render(
                request,
                'concordance_result.html',
                {
                    'form': form,
                    'data': data,
                    'query': request.POST,
                    'link_for_output': link_for_output
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

    @staticmethod
    def _segcom(txt):
        jraw = jieba.seg(txt, pos=True)
        jres, jpos = [], []
        for char, pos in jraw:
            if char != '\n':
                jres.append(char)
                jpos.append(pos)
        cres, cpos = [], []
        craw = ckip.seg(txt).res
        for char, pos in craw:
            if char != '\n':
                cres.append(char)
                cpos.append(pos)
        if (
            len(''.join(jres).replace(' ', '')) !=
            len(''.join(cres).replace(' ', ''))
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
        for n, i in enumerate(idxcon_j):
            idxs = [int(j) for j in i.split('_') if j != '']
            recv = ''.join([source[idx] for idx in idxs])
            if i in ovlps:
                output_j += recv
            else:
                output_j += f'<span class="diff">{recv}|{jpos[n]}</span>'
            output_j += ' '
        for n, i in enumerate(idxcon_c):
            idxs = [int(j) for j in i.split('_') if j != '']
            recv = ''.join([source[idx] for idx in idxs])
            if i in ovlps:
                output_c += recv
            else:
                output_c += f'<span class="diff">{recv}|{cpos[n]}</span>'
            output_c += ' '
        return (output_j, output_c)


def sentipol(request):
    """Sentipol page."""
    return render(request, 'sentipol.html')


def wordcloud(request):
    """Wordcloud page."""
    return render(request, 'wordcloud.html')
