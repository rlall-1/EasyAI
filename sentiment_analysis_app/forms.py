from django import forms

class SentimentEntryForm(forms.Form):
    stock_symbl = forms.CharField(max_length=10,min_length=2,empty_value='')
    sentiment_txt = forms.CharField(max_length=15,min_length=2,empty_value='')

