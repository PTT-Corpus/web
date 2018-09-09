"""Core app forms."""
import ast

from django import forms
from material import Layout, Row, Column, Fieldset


class ConcordanceForm(forms.Form):
    """Concordance form."""

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
        required=False,
    )
    start.widget.attrs['class'] = 'datepicker'
    end = forms.DateField(
        label='End',
        required=False,
    )
    end.widget.attrs['class'] = 'datepicker'
    pos = forms.BooleanField(
        label='',
        required=False,
    )
    window_size = forms.IntegerField(
        label='',
        initial=10,
    )
    page = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False,
    )
    size = forms.IntegerField(
        label='',
        initial=10,
        required=False,
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
                Fieldset('Sort', 'sort'),
                Fieldset('Order', 'order'),
                Fieldset('Items per Page', 'size'),
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
        boards = cleaned_data.get('boards')
        if boards:
            cleaned_data['boards'] = ','.join(ast.literal_eval(boards))
        return cleaned_data
