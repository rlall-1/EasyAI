from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class UserFileInfo(models.Model):
    file_description = models.CharField(max_length=255, blank=True)
    # file_uploaded_by_user = models.FileField(upload_to='userfiles', verbose_name="Select file to analyze",  validators=[FileExtensionValidator(['csv'])])
    file_uploaded_by_user = models.FileField(upload_to='userfiles', verbose_name="Select file to analyze")
    file_independent_columns_list = models.CharField(max_length=355, blank=True)
    file_dependent_column_name = models.CharField(max_length=255, blank=True)
    file_unsupervised_learning = models.BooleanField(verbose_name="Unsupervised learning?", default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

class UserModelDetails(models.Model):
    user_File_id = models.ForeignKey(UserFileInfo, on_delete=models.CASCADE)
    # scatter_digImage_name = models.ImageField(upload_to='model_generated_app')
    scatter_digImage_name = models.CharField(max_length=255, blank=True)
    generated_model_name=models.CharField(max_length=255, blank=True)
    url_Prefix=models.CharField(max_length=355, blank=True)

    def __str__(self):
        return self.id  

