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
        csv_data = csv_file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(csv_data))
        df_limited = df.head(100)
        context={
            'df': df,
            'df_limited': df_limited,
        }
        request.session['df'] = df.to_json(orient='records')
        request.session['df_limited'] = df_limited.to_json(orient='records')
        return render(request,'upload.html',context=context)
    else:
        return HttpResponse('Invalid request.')

def handle_dropdown(request):
    df_json = request.session.get('df')
    df_limited_json = request.session.get('df_limited')
    df = pd.read_json(df_json)
    df_limited = pd.read_json(df_limited_json)
    if request.method == 'POST':
        selected_column=request.POST.get('selectedColumn', '')
        context={
            'df': df,
            'df_limited': df_limited,
            'selected_column':selected_column,
        }
        return render(request,'get_column.html',context=context)