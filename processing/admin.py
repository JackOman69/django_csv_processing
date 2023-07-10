from typing import Any, List
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.http.request import HttpRequest
from processing.models import CSVFileData, CSVFile

class CSVFileDataInline(admin.StackedInline):
    model = CSVFileData
    extra = 0
    fields = ["customer", "item", "total", "quantity"]
        
class CSVFileAdmin(admin.ModelAdmin):
    model = CSVFile
    fields = ["csv_file"]
    readonly_fields = ["csv_file"]

    def get_inline_instances(self, request: HttpRequest, obj: Any | None = ...):
        self.inlines = [CSVFileDataInline, ]
        return super(CSVFileAdmin, self).get_inline_instances(request, obj)
    
admin.site.register(CSVFile, CSVFileAdmin)