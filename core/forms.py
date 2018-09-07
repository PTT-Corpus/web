"""Core app forms."""
import datetime

from django import forms
from material import Layout, Row, Column, Fieldset


class ConcordanceForm(forms.Form):
    """Concordance form."""

    YEAR_CHOICES = [
        str(y)
        for y
        in range(2005, datetime.datetime.now().year + 1)
    ]

    word = forms.CharField(
        max_length=255,
        label='',
    )
    post_type = forms.CharField(
        label='',
        widget=forms.RadioSelect(choices=(
            (0, "Posts"),
            (1, "Comments"),
        ))
    )
    boards = forms.CharField(
        label='',
        widget=forms.CheckboxSelectMultiple(choices=(
            ('Gossiping', '八卦板'),
            ('joke', '就可板'),
            ('movie', '電影板'),
        )),
        required=False,
    )
    sort = forms.CharField(
        label='',
        widget=forms.RadioSelect(choices=(
            ('published', 'Publish Time'),
            ('upvote', 'Likes (推)'),
            ('downvote', 'Dislikes (噓)'),
        )),
    )
    order = forms.CharField(
        label='',
        widget=forms.RadioSelect(choices=(
            ('desc', 'Descending'),
            ('asc', 'Ascending')
        )))
    start = forms.DateField(
        label='Start',
        widget=forms.SelectDateWidget(years=YEAR_CHOICES)
    )
    end = forms.DateField(
        label='End',
        widget=forms.SelectDateWidget(years=YEAR_CHOICES),
        initial=datetime.datetime.now
    )
    pos = forms.BooleanField(
        label='Part of Speech',
        required=False,
    )
    window_size = forms.IntegerField(
        label='',
        initial=5,
    )

    layout = Layout(
        Row(
            Column(
                Fieldset('Query Word', 'word'),
                Fieldset('Boards', 'boards'),
                Fieldset('Window Size', 'window_size'),
                Fieldset('Post Type', 'post_type'),
                span_columns=6,
            ),
            Column(
                Fieldset('Part of Speech', 'pos'),
                Fieldset('Order', 'order'),
                Fieldset('Sort', 'sort'),
                Fieldset('Date range', 'start', 'end'),
                span_columns=6,
            ),
        ),
    )

    def clean(self):
        """Process form data."""
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        if (start and end) and (start > end):
            raise forms.ValidationError(
                "End date cannot be earlier than start date.")
        return cleaned_data
