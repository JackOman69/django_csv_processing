from django.urls import re_path, path

from processing.views import CSVFileApiView, ExactCSVFileApiView

urlpatterns = [
    re_path(r"^process/$", CSVFileApiView.as_view(), name="csv"),
    path("get_csv/<int:id>", ExactCSVFileApiView.as_view({"get": "retrieve"}), name="single_csv")
]