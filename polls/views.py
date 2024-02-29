from django.shortcuts import render
from django.http import HttpResponse
import csv
import pandas as pd
import io

# Create your views here.
def index(request):
    return render(request,'index.html')

def handle_csv_upload(request):
    if request.method == 'POST' and request.FILES['csvFile']:
        csv_file = request.FILES['csvFile']

        if not csv_file.name.endswith('.csv'):
            return HttpResponse('Invalid file. Please upload a CSV file.')

        csv_data = csv_file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(csv_data))
        return render(request,'upload.html')
    else:
        return HttpResponse('Invalid request.')
