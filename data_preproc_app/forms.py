from django import forms
from data_upload_app.models import UserFileInfo

class PreProcessForm(forms.Form):
    colMissingDataNames = forms.MultipleChoiceField(label="Select the columns that have missing data", choices=[], required=False)
    blank_data_strategy = forms.ChoiceField(label = "Select the strategy to handle missing data", 
                                choices=[("mean", "Mean"),
                                ("median", "Median"),
                                ("most_frequent", "Most  Frequent ")
                            ])
    training_set_ratio = forms.ChoiceField(label = "Select the percentage size of the training data", 
                                choices=[(0.7, "70%"),
                                (0.8, "80%"),
                            ])
    # dependent_col_Encode = forms.ChoiceField(label = "Select the Dependent Column in the dataset", choices=[])
    dependent_col_Encode = forms.BooleanField(label = "Encode the Dependent Column?", required=False)
    colNames = forms.MultipleChoiceField(label="Select the Columns to encode (if any)", choices=[], required=False)

    alogorithm_to_use = forms.ChoiceField(label = "Select the Alogorithm to use", 
                                choices=[("LinearRegression", "Linear Regression"),
                                ("XGBoostR", "XGBoost - Regression"),
                                ("XGBoostC", "XGBoost - Classification"),
                                ])
                                

    def __init__(self, pk, data=None, files=None, auto_id='id_%s', prefix=None, initial=None,  label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None, renderer=None):
        super().__init__(data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial,  label_suffix=label_suffix, empty_permitted=empty_permitted, field_order=field_order, use_required_attribute=use_required_attribute, renderer=renderer)

        fileRecord = UserFileInfo.objects.get(id=pk)
        colList = fileRecord.file_independent_columns_list.split(',')
        # colList = fileRecord.file_independent_columns_list
        colNum = 0
        colChoices=[]
        for colName in colList:
            colChoices.append((colNum, colName))
            colNum = colNum + 1
         
        self.fields['colMissingDataNames']=forms.MultipleChoiceField(choices=colChoices , label = "Select the columns that have missing data", required=False)
        self.fields['colNames']=forms.MultipleChoiceField(choices=colChoices , label = "Select the column to encode", required=False)
        # self.fields['dependent_col_Name']=forms.ChoiceField(choices=colChoices , label = "Select the Dependant column")

