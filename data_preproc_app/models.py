from django.db import models
from data_upload_app import models as uploadapp_Model

# Create your models here.

class UserFileEncoded(models.Model):
    file_id = models.ForeignKey(uploadapp_Model.UserFileInfo, on_delete=models.CASCADE)
    cols_encoded = models.CharField(max_length=400, blank=True)
    encoded_file_location=models.FileField(upload_to='encoded_files')
    

 



    def __str__(self):
        return self.name
