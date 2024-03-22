from django import forms
from data_upload_app.models import UserFileInfo

class UploadFileForm(forms.ModelForm):

    class Meta:
        model = UserFileInfo
        fields = ('file_description', 'file_unsupervised_learning', 'file_uploaded_by_user')
        