"""Core app forms."""
from django import forms
from material import Layout, Row, Column, Span
from .data import boards as b

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
        label='Query',
        help_text='可使用CQL查詢或一般查詢'
    )

    cql_enable = forms.BooleanField(
        label='使用CQL模式',
        widget=forms.CheckboxInput(),
        required=False,
    )


    post_type = forms.CharField(
        label='搜尋對象',
        widget=forms.RadioSelect(
            choices=(
                (0, "找全部"),
                (1, "只找標題"),
                (2, "只找內文"),
                (3, "只找回文: 推文"),
                (4, "只找回文: 噓文"),
                (5, "只找回文: 箭頭文"),
                (6, "只找回文: 所有回文"),
            ), 
            # attrs={"disabled":"disabled"}
        ),
        required=True,
    )

    boards = forms.CharField(
        label='找哪個版',
        widget=forms.Select(
            choices=b
        )
    )
    # boards = forms.CharField(
    #    label='Boards',
    #    widget=forms.HiddenInput(
    #        attrs={'type': 'hidden'},
    #    ),
    #    initial='LGBT_SEX',
    #    required=False,
    #)
    #    sort = forms.CharField(
    #        label='Sort',
    #        widget=forms.RadioSelect(choices=(
    #            ('published', 'Publish Time'),
    #            ('upvote', 'Likes (推)'),
    #            ('downvote', 'Dislikes (噓)'),
    #        )),
    #    )
    #    order = forms.CharField(
    #        label='Order',
    #        widget=forms.RadioSelect(choices=(
    #            ('desc', 'Descending'),
    #            ('asc', 'Ascending')
    #        )))
    start = forms.IntegerField(
        label='起始年份',
        min_value=2001,
        max_value=2020,
        initial=2020,
        # required=False,
    )
    # start.widget.attrs['class'] = 'datepicker'
    end = forms.IntegerField(
        label='結束年份',
        min_value=2001,
        max_value=2020,
        initial=2020,
        # required=False,
    )
    # end.widget.attrs['class'] = 'datepicker'
    pos = forms.BooleanField(
        label='顯示詞性',
        widget=forms.CheckboxInput(),
        required=False,
    )
    window_size = forms.IntegerField(
        label='視窗大小',
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 5, 'max': 30}),
        initial=10,
    )
    page = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False,
    )
    size = forms.IntegerField(
        label='每頁顯示筆數',
        widget=forms.NumberInput(
            attrs={'type': 'range', 'min': 10, 'max': 100, 'step': 10}
        ),
        initial=50,
        required=False,
    )

    layout = Layout(
        Row(
            Column(
                'word',
                'cql_enable',
                'boards',
                Row(
                    Span(6, 'post_type'),
                    Span(6, 'pos')
                    # Span(4, 'sort'),
                    # Span(4, 'order'),
                ),
                span_columns=6,
            ),
            Column(
                # 'pos',
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
                "起始年份不得晚於結束年份！")
        return cleaned_data
