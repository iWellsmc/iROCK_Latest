from django import forms
from .models import Fileupload


class FileUploadForm(forms.ModelForm):
    document=forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Fileupload
        fields = ('document',) 
