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

def out():
    pass

def process_parameter_form(request):
    session_value = request.session.get('type', None)
    
    if request.method == 'POST':
        # Get the number of parameters from the form
        num_parameters = int(request.POST.get('numParameters', 0))

        # Extract parameter names and types from the form data
        parameter_data = []
        for i in range(1, num_parameters + 1):
            param_name = request.POST.get(f'parameter{i}_name', '')
            param_type = request.POST.get(f'parameter{i}_type', '')
            parameter_data.append({'name': param_name, 'type': param_type})

        # Process the extracted data as needed
        request.session['params'] = parameter_data

        # Create Gradio Interface based on input components
        input_components = []
        for param in parameter_data:
            if param['type'] == 'string':
                input_components.append(gr.Text(label=param['name']))
            elif param['type'] == 'int':
                input_components.append(gr.Number(label=param['name']))
            else:
                input_components.append(gr.Number(label=param['name']))
                
        loaded_model = pickle.load(open('static/models/your_model.pkl', 'rb'))

        # Create Gradio Interface
        interface = gr.Interface(
            fn=loaded_model.predict([input_components]),
            inputs=input_components,
            outputs="label",  # Replace with your actual output type
        )

        # Share the Gradio interface and get the public URL
        interface_url = interface.launch(share=True)

        # Save the Gradio interface URL in the session
        request.session['gr_interface_url'] = interface_url

        # Redirect to the Gradio interface page
        return redirect('gradio_interface')

    return HttpResponse('Invalid request method')

def gradio_interface(request):
    # Retrieve the Gradio interface URL from the session
    gr_interface_url = request.session.get('gr_interface_url')

    if gr_interface_url:
        # Render the Django template with the Gradio interface URL
        return render(request, 'gradio_template.html', {'gr_interface_url': gr_interface_url})

    return HttpResponse('Gradio interface URL not found in session.')