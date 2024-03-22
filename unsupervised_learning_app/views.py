from django.shortcuts import render
from data_upload_app.models import UserFileInfo, UserModelDetails

import pandas as pd
import numpy as np



# Create your views here.
def index(request, pk):

    user_record = UserFileInfo.objects.get(id=pk)
    
    dataset = pd.read_csv(user_record.file_uploaded_by_user, header=None)
    dataset_sample_list = dataset.head().values.tolist()

    context={
        'dataset_sample_list':dataset_sample_list,

    }



    return render(request,'unsupervised_learning_app/data_preview.html', context)