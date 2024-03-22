from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from data_upload_app import forms

# Create your views here.
def home(request):
    if request.method == "GET":
        return render(request,'data_upload_app/home.html', {'user_file_upload_form': forms.UploadFileForm()})
    else:
        # Create a form instance and populate it with data from the request (binding):
        form = forms.UploadFileForm(request.POST, request.FILES)
        # Check if the form is valid:
        if form.is_valid():
            try:
                isUnsupervisedLearning = form.cleaned_data['file_unsupervised_learning'] 
                new_data_upload = form.save(commit=True)
                # Above creates a new object. new_data_upload creates details of the object created
                pk = new_data_upload.id
                if isUnsupervisedLearning == True:
                     return redirect('/unsupervised_learning_app/' + str(pk)) 
                else:
                    return redirect('/data_preproc_app/' + str(pk)) 
            except :
                return render(request,'data_upload_app/home.html', {'user_file_upload_form': forms.UploadFileForm(), 'error': 'An error occured. Please try again'})


def faq(request):
     if request.method == "GET":
        return render(request,'faq.html')

def aboutme(request):
     if request.method == "GET":
        return render(request,'aboutme.html')

        
        