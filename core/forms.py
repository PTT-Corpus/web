"""Core app forms."""
from django import forms
from material import Layout, Row, Column, Span


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
        widget=forms.HiddenInput(
            attrs={'type': 'hidden'},
        ),
        initial='Gossiping,joke',
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
        widget=forms.CheckboxInput(),
        required=False,
    )
    window_size = forms.IntegerField(
        label='Window Size',
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 5, 'max': 30}),
        initial=10,
    )
    page = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False,
    )
    size = forms.IntegerField(
        label='Item per Page',
        widget=forms.NumberInput(
            attrs={'type': 'range', 'min': 10, 'max': 100, 'step': 10}
        ),
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
        return cleaned_data
