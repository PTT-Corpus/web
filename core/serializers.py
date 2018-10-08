from rest_framework import serializers


SEG_CHOICES = (
    ('Jseg', 'Jseg'),
    ('PyCCS', 'PyCCS'),
    ('Segcom', 'Segcom'),
)

POST_TYPE_CHOICES = (
    (0, 'Posts'),
    (1, 'Comments'),
    (None, 'All')
)

SORT_CHOICES = (
    ('published', 'Publish Time'),
    ('upvote', 'Likes (推)'),
    ('downvote', 'Dislikes (噓)'),
)

ORDER_CHOICES = (
    ('desc', 'Descending'),
    ('asc', 'Ascending'),
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

    def create(self, validated_data):
        """
        Satisfy abstract methods requirement.
        :param validated_data:
        :return:
        """

    def update(self, instance, validated_data):
        """
        Satisfy abstract methods requirement.
        :param instance:
        :param validated_data:
        :return:
        """


class ConcordanceSerializer(serializers.Serializer):
    word = serializers.CharField(
        label='Query Word',
        max_length=255,
        required=True,
    )
    post_type = serializers.ChoiceField(
        label='Post Type',
        choices=POST_TYPE_CHOICES,
        required=False,
    )
    boards = serializers.CharField(
        label='Boards',
        initial='Gossiping,joke',
        required=False,
    )
    sort = serializers.ChoiceField(
        label='Sort',
        choices=SORT_CHOICES,
    )
    order = serializers.ChoiceField(
        label='Order',
        choices=ORDER_CHOICES,
    )
    start = serializers.DateField(
        label='Start Date',
        required=False,
    )
    end = serializers.DateField(
        label='End Date',
        required=False,
    )
    pos = serializers.BooleanField(
        label='Part of Speech',
        required=False,
    )
    windows_size = serializers.IntegerField(
        label='Window Size',
        min_value=5,
        max_value=30,
        initial=10,
    )
    # page = serializers.HiddenField(
    #     required=False
    # )
    size = serializers.IntegerField(
        label='Items per page',
        min_value=10,
        max_value=100,
        initial=10,
        required=False
    )

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        start = validated_data.get('start')
        end = validated_data.get('end')
        if (start and end) and (start > end):
            raise serializers.ValidationError(
                "End date cannot be earlier than start date."
            )
        return validated_data

    def create(self, validated_data):
        """
        Satisfy abstract methods requirement.
        :param validated_data:
        :return:
        """

    def update(self, instance, validated_data):
        """
        Satisfy abstract methods requirement.
        :param instance:
        :param validated_data:
        :return:
        """
