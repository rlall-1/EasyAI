from rest_framework import serializers

from data_upload_app.models import UserModelDetails


class UserModelDetailsSerializer (serializers.ModelSerializer):
    class Meta:
        model = UserModelDetails
        fields = ['user_File_id', 'url_Prefix', 'generated_model_name']
        
