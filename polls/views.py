from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import csv
import pandas as pd
import io 
# import pycaret.regression as pr
import os
# import pycaret.classification as pc
import pickle
import sklearn
from sklearn.base import is_classifier, is_regressor
import tempfile
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import gradio as gr
from django.middleware.csrf import get_token
import concurrent.futures


def get_csrf_token(request):
    csrf_token=get_token(request)
    return JsonResponse({'csrfToken':csrf_token})

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
        # Create a temporary file to save the uploaded content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in pkl_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            # Load the model from the temporary file
            with open(temp_file_path, 'rb') as f:
                model = pickle.load(f)
            # Perform checks on the model type
            with open('static/models/your_model.pkl', 'wb') as file:
                pickle.dump(model, file)

            
            if is_classifier(model):
                request.session['type'] = 'classifier'
                return render(request, 'upload.html')
            elif is_regressor(model):
                request.session['type'] = 'regressor'
                return render(request, 'upload.html')
            else:
                return HttpResponse('Loaded model type cannot be determined.')
            
        
        except Exception as e:
            return HttpResponse(f'Error loading the model: {str(e)}')

        finally:
            # Delete the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

import pickle
import gradio as gr
import concurrent.futures
from django.shortcuts import render, redirect
from django.http import HttpResponse

def launch_gradio_interface(interface):
    interface_url = interface.launch(share=True)
    return interface_url

def process_parameter_form(request):
    if request.method == 'POST':
        # Extract parameter names and types from the form data
        num_parameters = int(request.POST.get('numParameters', 0))
        parameter_data = []
        for i in range(1, num_parameters + 1):
            param_name = request.POST.get(f'parameter{i}_name', '')
            param_type = request.POST.get(f'parameter{i}_type', '')
            parameter_data.append({'name': param_name, 'type': param_type})

        request.session['params'] = parameter_data

        # Create Gradio Input Components
        input_components = []
        for param in parameter_data:
            if param['type'] == 'string':
                input_components.append(gr.Textbox(label=param['name']))
            elif param['type'] == 'int':
                input_components.append(gr.Number(label=param['name']))
            else:
                input_components.append(gr.Number(label=param['name']))

        # Load the model
        loaded_model = pickle.load(open('static/models/your_model.pkl', 'rb'))

        # Create Gradio Interface
        interface = gr.Interface(
            fn=loaded_model.predict,
            inputs=input_components,
            outputs="text", 
            # Replace with your actual output type
        )

        # Use concurrent.futures to run launch_gradio_interface in a separate thread
        with concurrent.futures.ThreadPoolExecutor() as executor:
            interface_url = executor.submit(launch_gradio_interface, interface).result()

        # Redirect to the public Gradio interface URL
        return redirect(interface_url)

    return HttpResponse('Invalid request method')