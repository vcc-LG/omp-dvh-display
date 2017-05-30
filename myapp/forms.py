from django import forms

from .models import DVHDump

class DVHDumpForm(forms.ModelForm):
    class Meta:
        model = DVHDump
        fields = ('dump',)
