from django import forms
from core.models import NewsUsers

class NewsUserForm(forms.ModelForm):
    class Meta:
        model = NewsUsers
        fields = ['email']

