import os
import requests

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from jseg import Jieba
from ckip import CkipSegmenter

from .serializers import SegmentationSerializer
from .forms import SegmentationForm, ConcordanceForm
from .views import SegmentationFormView

_segcom = SegmentationFormView._segcom
jieba = Jieba()
ckip = CkipSegmenter()


@api_view(['POST'])
def segment(request, format=None):
    if request.method == 'POST':
        # serializer = SegmentationSerializer(data=request.data)
        # if serializer.is_valid():
        #     algo = serializer.validated_data.get('algo')
        #     text = serializer.validated_data.get('text')
        form = SegmentationForm(data=request.data)
        if form.is_valid():
            algo = form.cleaned_data.get('algo')
            text = form.cleaned_data.get('text')
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
                output = _segcom(text)
            return Response({'algo': algo, 'output': output})

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def concordance(request, format=None):
    if request.method == 'POST':
        form = ConcordanceForm(request.data)
        if form.is_valid():
            resp = requests.get(
            os.environ.get('PTT_ENGINE') + 'query',
                {k: v for k, v in form.cleaned_data.items() if v},
            )
            data = resp.json()
            return Response({
                'data': data,
                'query': request.POST
            })

    return Response(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)