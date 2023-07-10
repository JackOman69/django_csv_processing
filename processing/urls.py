from django.urls import re_path

from processing.views import CSVFileApiView

urlpatterns = [
    re_path(r"^process/$", CSVFileApiView.as_view(), name="csv")
]