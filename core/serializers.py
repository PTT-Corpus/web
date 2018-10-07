from rest_framework import serializers


SEG_CHOICES = (
    ('Jseg', 'Jseg'),
    ('PyCCS', 'PyCCS'),
    ('Segcom', 'Segcom'),
)


class SegmentationSerializer(serializers.Serializer):
    text = serializers.CharField(
        label='Input Text',
        style={'base_template': 'textarea.html'},
        required=True,
    )
    algo = serializers.ChoiceField(
        label='Algorithms',
        choices=SEG_CHOICES,
        required=True,
    )
