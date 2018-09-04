from django import forms
import datetime


class ConcordanceForm(forms.Form):
    POST = 0
    COMMENT = 1
    POST_TYPE_CHOICES = (
        (POST, "Posts"),
        (COMMENT, "Comments"),
    )

    DESCENDING = 'desc'
    ASCENDING = 'asc'
    ORDER_CHOICES = (
        (DESCENDING, 'Descending'),
        (ASCENDING, 'Ascending')
    )
    YEAR_CHOICES = [str(y) for y in range(2000, datetime.datetime.now().year + 1)]

    word = forms.CharField(max_length=255)
    page = forms.IntegerField()
    size = forms.IntegerField(help_text="Number of items to be shown on a page.")
    post_type = forms.CharField(widget=forms.RadioSelect(choices=POST_TYPE_CHOICES))
    boards = forms.Textarea()
    sort = forms.CharField(max_length=255)
    order = forms.CharField(widget=forms.RadioSelect(choices=ORDER_CHOICES))
    start_date = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES))
    end_date = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES),
                               initial=datetime.datetime.now)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     start_date = cleaned_data.get('start_date')
    #     print("="*40, type(start_date))
    #     end_date = cleaned_data.get('end_date')
    #
    #     if start_date > end_date:
    #         raise forms.ValidationError("End date cannot be earlier than start date.")
    #
    #     return cleaned_data

