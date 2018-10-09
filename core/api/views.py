import os
import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from jseg import Jieba
from ckip import CkipSegmenter

from core.serializers import SegmentationSerializer, ConcordanceSerializer
from core.views import SegmentationFormView

_segcom = SegmentationFormView._segcom
jieba = Jieba()
ckip = CkipSegmenter()


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'concordance': reverse('api:concordance', request=request, format=format),
        'segmentation': reverse('api:segmentation', request=request, format=format),
    })


class ConcordanceView(generics.GenericAPIView):
    """
    Return concordance lines for a given query.
    """
    serializer_class = ConcordanceSerializer

    def post(self, request, format=None):
        serializer = ConcordanceSerializer(data=request.data)
        if serializer.is_valid():
            resp = requests.get(
                os.environ.get('PTT_ENGINE') + 'query',
                {k: v for k, v in serializer.validated_data.items() if v},
            )
            data = resp.json()
            return Response({
                'data': data,
                'query': request.data,
            },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SegmentationView(generics.GenericAPIView):
    """
    Return a segmented string based on input.
    """
    serializer_class = SegmentationSerializer

    def post(self, request, format=None):
        serializer = SegmentationSerializer(data=request.data)
        if serializer.is_valid():
            algo = serializer.validated_data.get('algo')
            text = serializer.validated_data.get('text')
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
            return Response({'algo': algo, 'output': output},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
