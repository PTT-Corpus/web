"""Core app forms."""
import ast

from django import forms
from material import Layout, Row, Column, Span


class SegmentationForm(forms.Form):
    """Segmentation form."""

    text = forms.CharField(
        label='Input Text',
        widget=forms.Textarea(),
        required=True,
    )
    algo = forms.CharField(
        label='Algorithms',
        widget=forms.RadioSelect(
            choices=(
                ('Jseg', 'Jseg'),
                ('PyCCS', 'PyCCS'),
                ('Segcom', 'Segcom'),
            ),
        ),
        required=True,
    )

    layout = Row(
        Column(
            'text',
            span_columns=6,
        ),
        Column(
            'algo',
            span_columns=6,
        ),
    )


class ConcordanceForm(forms.Form):
    """Concordance form."""

    word = forms.CharField(
        max_length=255,
        label='Query Word',
    )
    post_type = forms.CharField(
        label='Post Type',
        widget=forms.RadioSelect(choices=(
            (0, "Posts"),
            (1, "Comments"),
            (None, "All"),
        )),
        required=False,
    )
    boards = forms.CharField(
        label='Boards',
        widget=forms.CheckboxSelectMultiple(choices=(
            ('Gossiping', '八卦板'),
            ('joke', '就可板'),
            ('movie', '電影板'),
        )),
        required=False,
    )
    sort = forms.CharField(
        label='Sort',
        widget=forms.RadioSelect(choices=(
            ('published', 'Publish Time'),
            ('upvote', 'Likes (推)'),
            ('downvote', 'Dislikes (噓)'),
        )),
    )
    order = forms.CharField(
        label='Order',
        widget=forms.RadioSelect(choices=(
            ('desc', 'Descending'),
            ('asc', 'Ascending')
        )))
    start = forms.DateField(
        label='Start Date',
        required=False,
    )
    start.widget.attrs['class'] = 'datepicker'
    end = forms.DateField(
        label='End Date',
        required=False,
    )
    end.widget.attrs['class'] = 'datepicker'
    pos = forms.BooleanField(
        label='Part of Speech',
        required=False,
    )
    window_size = forms.IntegerField(
        label='Window Size',
        initial=10,
    )
    page = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False,
    )
    size = forms.IntegerField(
        label='Item per Page',
        initial=10,
        required=False,
    )

    layout = Layout(
        Row(
            Column(
                'word',
                'boards',
                Row(
                    Span(4, 'post_type'),
                    Span(4, 'sort'),
                    Span(4, 'order'),
                ),
                span_columns=6,
            ),
            Column(
                'pos',
                Row(
                    Span(6, 'window_size'),
                    Span(6, 'size'),
                ),
                Row(
                    Span(6, 'start'),
                    Span(6, 'end'),
                ),
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
        boards = cleaned_data.get('boards')
        if boards:
            cleaned_data['boards'] = ','.join(ast.literal_eval(boards))
        return cleaned_data
