from django import forms
from django.forms import widgets


class sendMessageForm(forms.Form):
    file = forms.FileField(required=False)
    message = forms.CharField()
    keyboards = forms.CharField(label="Tugmalar", required=False, widget=widgets.Textarea())
