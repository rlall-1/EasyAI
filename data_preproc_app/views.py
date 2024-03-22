from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from data_upload_app.models import UserFileInfo, UserModelDetails
from django.conf import settings

from .import forms


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder



def index(request, pk):

    if request.method=='POST':
        context = PreProcessFile(request)
        # return redirect('/model_generated_app/' + str(pk))
        # return redirect('/model_generated_app/model_preview.html' + str(pk))
        return render(request, 'model_generated_app/model_preview.html', context)   
    
    user_record = UserFileInfo.objects.get(id=pk)
    dataset = pd.read_csv(user_record.file_uploaded_by_user)
    dataset_description = dataset.describe()

    dataset_sample = dataset.head()
    
    

    # convert the dataframe to a list. This is so that we can use python for each in the templates
    datalist =  dataset_sample.values.tolist()
    colheaders = dataset_sample.columns.values.tolist()

    dataset_desc_list = dataset_description.values.tolist()
    dataset_desc_colheaders_list = dataset_description.columns.values.tolist()
    dataset_desc_index = dataset_description.index

    user_record.file_independent_columns_list = getColNames(dataset.columns.values[0:-1].tolist())
    user_record.file_dependent_column_name=dataset.columns.values[-1]
    user_record.save()
    
    display_preprocess_form = forms.PreProcessForm(pk)

    context={
        'dataframe': datalist,
        'colheaders':colheaders,
        'pk': pk,
        'display_preprocess_form': display_preprocess_form,
        'dataset_desc_list': dataset_desc_list,
        'dataset_desc_colheaders_list':dataset_desc_colheaders_list,
        'dataset_desc_index':dataset_desc_index,
        'dataset_description':dataset_description,
        
  
    }


    return render(request, 'data_preproc_app/data_preview.html', context)

def getColNames(col_list):
    # function returns comma separated col names
    col_Names=''
    for col_name in col_list:
        if col_Names=='':
            col_Names = col_name
        else:
            col_Names = col_Names + ',' + col_name
    return col_Names

def PreProcessFile(request):
    fileID = request.POST["FileID"]
    my_encode_form = forms.PreProcessForm(fileID, request.POST )
    if my_encode_form.is_valid() == False:
            print(' Errors are '+ str(my_encode_form.errors))
    
    if my_encode_form.is_valid():
            return GenerateModel(my_encode_form, fileID)

def GenerateModel(formSubmitted, FileID):
    colsWithMissingData = formSubmitted.cleaned_data.get('colMissingDataNames')
    colToEncode = formSubmitted.cleaned_data.get('colNames')
    dependent_col_Encode =formSubmitted.cleaned_data.get('dependent_col_Encode')
    training_set_ratio = formSubmitted.cleaned_data.get('training_set_ratio')
    alogorithm_to_use = formSubmitted.cleaned_data.get('alogorithm_to_use')

    user_record = UserFileInfo.objects.get(id=FileID)
    
    dataset = pd.read_csv(user_record.file_uploaded_by_user)


    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    # Handle the missing data
    for col_idx in colsWithMissingData:
        imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
        imputer.fit(X[:,int(col_idx)].reshape(-1,1))
        X[:,int(col_idx):int(col_idx)+1] = imputer.transform(X[:, int(col_idx)].reshape(-1,1))
    


    for col_idx in colToEncode:
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [int(col_idx)])], remainder='passthrough')
        X = np.array(ct.fit_transform(X))

    if dependent_col_Encode==True:
        le = LabelEncoder()
        y = le.fit_transform(y)
   


    # Now split the data into training and testing data

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = float(training_set_ratio), random_state=0)

    # Now build model

    import pickle
    import joblib
    import os
    USER_FILES_ROOT = getattr(settings, "USER_FILES_ROOT", None)

    if alogorithm_to_use=="LinearRegression":
        from sklearn.linear_model import LinearRegression
        regressor = LinearRegression()    
        # Below is where my model is being developed.
        regressor.fit(X_train, y_train)
        # Model developed. Now save this model.
        modelPath = os.path.join(USER_FILES_ROOT, "LinearRegressionModel" + str(FileID) + ".sav")
        model_name = "LinearRegressionModel" + str(FileID) + ".sav"
         # Save the model
        joblib.dump(regressor, modelPath,)
        # Update the user model table with location of the saved model
        userModelRecord = UserModelDetails.objects.create(user_File_id_id=FileID, generated_model_name = model_name)
         ## Now let us see how good our model is
        y_pred = regressor.predict(X_test)

        from sklearn.metrics import mean_squared_error
        import math

        rmse = math.sqrt(mean_squared_error(y_test, y_pred))

        plt.title("Model accuracy (RMSE) = " + str(rmse) )
        plt.xlabel("Test Data")
        plt.ylabel("Predicted Data")
        plt.scatter(y_test, y_pred)

        filePath = os.path.join(USER_FILES_ROOT, "image" + str(FileID) + ".png")
        plt.savefig(filePath)

        USER_FILES_URL = getattr(settings, "USER_FILES_URL", None)
        fileURL=    USER_FILES_URL + "image" + str(FileID) + ".png"
        userModelRecord.url_Prefix = USER_FILES_URL
        userModelRecord.save()
        model_save_location = USER_FILES_URL+model_name
        context={
            'pltFigURL':fileURL,
            'mdlDwnldLocation':model_save_location
        }
        return context
    elif alogorithm_to_use=="XGBoostR":
        from xgboost import XGBRegressor
        regressor = XGBRegressor()
        regressor.fit(X_train, y_train)
        modelPath = os.path.join(USER_FILES_ROOT, "XGBoostR" + str(FileID) + ".sav")
        model_name = "XGBoostR" + str(FileID) + ".sav"
        # Save the model
        joblib.dump(regressor, modelPath,)
        # Update the user model table with location of the saved model
        userModelRecord = UserModelDetails.objects.create(user_File_id_id=FileID, generated_model_name = model_name)
        model_id = userModelRecord.id

        ## Now let us see how good our model is
        y_pred = regressor.predict(X_test)

        from sklearn.metrics import explained_variance_score
        accuracy = explained_variance_score(y_test, y_pred)

        # plt.title("Model accuracy = " + str(accuracy) )
        plt.title("Model accuracy = %.2f%%" % (accuracy*100.0) )
        plt.xlabel("Test Data")
        plt.ylabel("Predicted Data")
        plt.scatter(y_test, y_pred)
        

        filePath = os.path.join(USER_FILES_ROOT, "image" + str(FileID) + ".png")
        plt.savefig(filePath)

        USER_FILES_URL = getattr(settings, "USER_FILES_URL", None)
        fileURL=    USER_FILES_URL + "image" + str(FileID) + ".png"
        userModelRecord.url_Prefix = USER_FILES_URL
        userModelRecord.save()
        model_save_location = USER_FILES_URL+model_name
        context={
            'pltFigURL':fileURL,
            'mdlDwnldLocation':model_save_location,
            'model_id':model_id,
        }
        return context

    elif alogorithm_to_use=="XGBoostC":
        from xgboost import XGBClassifier
        # from xgboost import plot_tree
        
        
        

        classifier = XGBClassifier()
        classifier.fit(X_train, y_train)
        
        
        # plot_tree(classifier)
        
        modelPath = os.path.join(USER_FILES_ROOT, "XGBoostC" + str(FileID) + ".sav")
        model_name = "XGBoostC" + str(FileID) + ".sav"
        # Save the model
        joblib.dump(classifier, modelPath,)
        # Update the user model table with location of the saved model
        userModelRecord = UserModelDetails.objects.create(user_File_id_id=FileID, generated_model_name = model_name)
         ## Now let us see how good our model is
        y_pred = classifier.predict(X_test)

        from sklearn.metrics import accuracy_score
        accuracy = accuracy_score(y_test, y_pred)

        plt.xlabel("Test Data")
        plt.ylabel("Predicted Data")
        plt.title("Model accuracy = %.2f%%" % (accuracy*100.0) )
        plt.scatter(y_test, y_pred)

        filePath = os.path.join(USER_FILES_ROOT, "image" + str(FileID) + ".png")
        plt.savefig(filePath)

        USER_FILES_URL = getattr(settings, "USER_FILES_URL", None)
        fileURL=    USER_FILES_URL + "image" + str(FileID) + ".png"
        userModelRecord.url_Prefix = USER_FILES_URL
        userModelRecord.save()
        model_save_location = USER_FILES_URL+model_name
        context={
            'pltFigURL':fileURL,
            'mdlDwnldLocation':model_save_location
        }
        return context
    
    
   

    """
    user_record = UserFileInfo.objects.get(id=FileID)
    user_record.model_Name = modelPath
    user_record.save()

    # Now we need to save the pre-processed Independent and Dependent variables in a csv.
    # We can use this later for calculating the accuracy of the model.

    
    ### independentVarsFilePath = os.path.join(USER_FILES_ROOT, "IndependentVars" + str(FileID) + ".csv")
    dependentVarsFilePath = os.path.join(USER_FILES_ROOT, "DependentVars" + str(FileID) + ".csv")
    


    pd.DataFrame(X).to_csv(independentVarsFilePath, index=False,header=False)
    pd.DataFrame(y).to_csv(dependentVarsFilePath, index=False,header=False)
    
    y_pred = regressor.predict(X_test)

    plt.xlabel("Test Data")
    plt.ylabel("Predicted Data")
    plt.scatter(y_test, y_pred)

    filePath = os.path.join(USER_FILES_ROOT, "image" + str(FileID) + ".png")

    plt.savefig(filePath)

    USER_FILES_URL = getattr(settings, "USER_FILES_URL", None)
    fileURL=    USER_FILES_URL + "image" + str(FileID) + ".png"

    userModel = UserModelDetails.objects.create(user_File_id_id=FileID, scatter_digImage = fileURL)

    


    return
    
    
    
    # load the model from disk
    loaded_model = joblib.load(modelPath)

    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state=0)

    result = loaded_model.score(X_test, y_test)
    
    return
    

    y_pred = regressor.predict(X_test)

    

    

    

    from sklearn import metrics

    metrics.mean_absolute_error(y_test, y_pred)
    metrics.mean_squared_error(y_test, y_pred)

    import seaborn as sns


    plt.xlabel("Test Data")
    plt.ylabel("Predicted Data")
    plt.scatter(y_test, y_pred)
   
    plt.savefig(fname="image")

    # sns.distplot((y_test - y_pred))
    
    return

    """
