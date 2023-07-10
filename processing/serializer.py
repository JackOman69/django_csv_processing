from rest_framework import serializers
from processing.models import CSVFile

class CSVSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CSVFile
        fields = ["csv_file"]