from django.shortcuts import render
from data_upload_app.models import UserFileInfo, UserModelDetails

from django.conf import settings 
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import joblib

# Create your views here.
def index(request, pk):
    
    user_record = UserFileInfo.objects.get(id=pk)
    modelName = user_record.model_Name

    USER_FILES_ROOT = getattr(settings, "USER_FILES_ROOT", None)
    independentVarsFilePath = os.path.join(USER_FILES_ROOT, "IndependentVars" + str(pk) + ".csv")
    dependentVarsFilePath = os.path.join(USER_FILES_ROOT, "DependentVars" + str(pk) + ".csv")

    datasetIndp = pd.read_csv(independentVarsFilePath)
    datasetDpndt = pd.read_csv(dependentVarsFilePath)

    X = datasetIndp.iloc[:, :].values
    y = datasetDpndt.iloc[:, :].values

    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.7, random_state=0)

    regressor = joblib.load(modelName)

    y_pred = regressor.predict(X_test)

    plt.xlabel("Test Data")
    plt.ylabel("Predicted Data")
    plt.scatter(y_test, y_pred)

    USER_FILES_ROOT = getattr(settings, "USER_FILES_ROOT", None)
    USER_FILES_URL = getattr(settings, "USER_FILES_URL", None)

    filePath = os.path.join(USER_FILES_ROOT, "image" + str(pk) + ".png")

    
    plt.savefig(filePath)

    fileURL=    USER_FILES_URL + "image" + str(pk) + ".png"
    

    userModel = UserModelDetails.objects.create(user_File_id_id=pk, scatter_digImage = fileURL)
    model_id = userModel.id

    

    


    

    result = regressor.score(X_test, y_test)

    context={
        'userModel': userModel,
        'filePath':fileURL,
        'model_id':model_id,
       
    }

    return render(request, 'model_generated_app/model_preview.html', context)
