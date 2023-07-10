import os
import csv
from datetime import datetime

from django.db import models

class CSVFile(models.Model):
    
    csv_file = models.FileField()
    
    class Meta:
        verbose_name = "CSV Файл"
        verbose_name_plural = "CSV Файлы"

class CSVFileData(models.Model):
    
    csv_file_source = models.ForeignKey(CSVFile, on_delete=models.CASCADE, verbose_name="CSV Файл парсинга", null=True)
    customer = models.CharField(max_length=255, verbose_name="Имя", default="", blank=True)
    item = models.CharField(max_length=255, verbose_name="Название камня", default="", blank=True)
    total = models.IntegerField(default=0, verbose_name="Общее количество", blank=True)
    quantity = models.IntegerField(default=0, verbose_name="Количество", blank=True)
    data = models.DateTimeField(auto_now_add=True, verbose_name="Дата", blank=True)
    
    class Meta:
        verbose_name = "Результат парсинга"
        verbose_name_plural = "Результаты парсинга"
        ordering = ("-data",)
    
