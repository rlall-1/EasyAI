
from rest_framework import generics
from data_upload_app.models import UserModelDetails
from .serializers import UserModelDetailsSerializer

# Create your views here.


class MLModel(generics.ListAPIView):
    serializer_class = UserModelDetailsSerializer
    #queryset = UserModelDetails.objects.get(pk=self)

    def get_queryset(self):
        # queryset = UserModelDetails.objects.get(id=self.kwargs['model_id'])
        # queryset = UserModelDetails.objects.get(id=67)
        # queryset = UserModelDetails.objects.filter(id=67)
        queryset = UserModelDetails.objects.filter(id=self.kwargs['model_id'])
        return queryset
        # return render(request, 'api/deployed_model.html', queryset) 
        

