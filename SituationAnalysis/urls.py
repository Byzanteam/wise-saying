from django.urls import re_path as url

from SituationAnalysis.views import FormDataView

urlpatterns = [
    url('situation/wisesay',FormDataView.as_view()),
]