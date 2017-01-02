from django import forms
from .models import Person

class NameForm(forms.ModelForm):
    name = forms.CharField(label="Name", max_length=128, required=True)
    class Meta:
        model = Person
        fields = ('name',)
