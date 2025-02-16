# myapp/forms.py
from django import forms
from .models import UserPreference

class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        exclude = ('user',) 
        fields = ['sources', 'topics', 'keywords']