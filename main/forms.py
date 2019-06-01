from django import forms

class IdForm(forms.Form):
    insid = forms.CharField(label='Your name', max_length=100)