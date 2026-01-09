from django.urls import path

from .views.SurveyFormViews import (
    SurveyFormCreateAPIView,
    SurveyFormListAPIView,
    SurveyFormUpdateAPIView,
    SurveyFormDetailAPIView
)



urlpatterns = [
    path('create', SurveyFormCreateAPIView.as_view(), name='survey-form-create'),
    path('', SurveyFormListAPIView.as_view(), name='survey-form-list'),
    path('<int:pk>/update', SurveyFormUpdateAPIView.as_view(), name='survey-form-update'),
    path('<int:pk>', SurveyFormDetailAPIView.as_view(), name='survey-form-detail'),
]