from django.urls import path
from . import views

urlpatterns = [
    path('<int:model_id>',views.MLModel.as_view()),
    
]