import csv
import os
import json
import pandas as pd
from datetime import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView

from csvprocessing.settings import BASE_DIR
from processing.models import CSVFile, CSVFileData
from processing.serializer import CSVSerializer

def parse_data_from_csv(query_set_object, status):
    if status == "all":
        csv_file = query_set_object.last()
    elif status == "single":
        csv_file = query_set_object
        
    data = pd.read_csv(csv_file.csv_file)
    
    grouped_data = data.groupby('customer')['total'].sum().reset_index()
    sorted_data = grouped_data.sort_values('total', ascending=False)
    top_customers = sorted_data.head(5)
    
    gems = data[data['customer'].isin(top_customers['customer'])]['item'].value_counts()
    gems = gems[gems >= 2].index.tolist()
    
    top_customers = json.loads(top_customers.to_json(orient='records'))
    
    return [top_customers, gems]
        

class CSVFileApiView(GenericAPIView):
    
    queryset = CSVFile.objects.all()
    serializer_class = CSVSerializer
    
    @method_decorator(cache_page(60*15))
    def get(self, *args, **kwargs):
        sources = CSVFile.objects.all()
        result = {"response": []}
        
        top_customers, gems = parse_data_from_csv(query_set_object=sources, status="all")
        for customer in top_customers:
            customer["gems"] = gems
            result["response"].append(
                {
                    "username": customer["customer"],
                    "spent_money": customer["total"],
                    "gems": customer["gems"]
                }
            )
        return Response(result, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        csv_file = request.FILES["deals"]
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name, file_extension = os.path.splitext(csv_file.name)
        
        csv_file.name = f"{file_name}_{timestamp}{file_extension}"
        if not csv_file.name.endswith(".csv"):
            return Response(
                {"Status": "Error", "Desc": "Неподдерживаемый формат файла - в процессе обработки файла произошла ошибка"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        file_path = os.path.join(BASE_DIR, "persistentdata", "media")
        
        serializer = CSVSerializer(data={"csv_file": csv_file})
        if serializer.is_valid():
            serializer.save()
            with open(file=f"{file_path}/{csv_file.name}", encoding="utf-8") as file:
                csv_data = csv.DictReader(file)
                csv_file_instance = CSVFile.objects.get(csv_file=csv_file)
                for row in csv_data:   
                    CSVFileData.objects.create(
                        csv_file_source=csv_file_instance,
                        customer=row["customer"],
                        item=row["item"],
                        total=int(row["total"]),
                        quantity=int(row["quantity"]),
                        data=datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S.%f")
                    )
            return Response(
                {"Status": "OK"},
                status=status.HTTP_201_CREATED
            )
            
        
        return Response(
            {"Status": "Error", "Desc": f"{serializer.errors} - в процессе обработки файла произошла ошибка"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
class ExactCSVFileApiView(viewsets.ViewSet):
    
    serializer_class = CSVSerializer
    
    @method_decorator(cache_page(60*15))
    @action(detail=True, methods=["get"])
    def retrieve(self, request, id):
        try:
            source = CSVFile.objects.get(id=id)
        except CSVFile.DoesNotExist:
            return Response(
                {"Status": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        result = {"response": []}
        
        top_customers, gems = parse_data_from_csv(query_set_object=source, status="single")
        for customer in top_customers:
            customer["gems"] = gems
            result["response"].append(
                {
                    "username": customer["customer"],
                    "spent_money": customer["total"],
                    "gems": customer["gems"]
                }
            )
        return Response(result, status=status.HTTP_200_OK)