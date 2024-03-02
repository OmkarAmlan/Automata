from django.shortcuts import render
from django.http import HttpResponse
import csv
import pandas as pd
import io 
import pycaret.regression as pr
import pycaret.classification as pc
import pickle

def remove_percent_symbol(entry):
    if isinstance(entry, str) and '%' in entry:
        valid_entries = entry.rstrip('%')
        if valid_entries.isdigit():
            return int(valid_entries)
    return entry

def remove_currency_symbol(entry):
    if isinstance(entry, str) and entry.startswith('$'):
        valid_entries = entry[1:]
        if valid_entries.isdigit():
            return int(valid_entries)
    return entry

def remove_symbols_from_all_columns(df):
    df = df.applymap(remove_percent_symbol).applymap(remove_currency_symbol)

    # Convert categorical columns to numeric
    for col in df.select_dtypes(include='category').columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df
def index(request):
    return render(request,'index.html')

def handle_pkl_upload(request):
    if request.method == 'POST' and request.FILES['pklFile']:
        pkl_file = request.FILES['pklFile']
        context={
            'pkl_file': pkl_file,
        }
        
        return render(request,'upload.html',context=context)
    else:
        return HttpResponse('Invalid request.')

