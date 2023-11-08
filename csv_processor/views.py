import csv
import hashlib
from io import TextIOWrapper
import os
import shutil
import zipfile
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd

from CsvProcessingApp import settings
from .models import ProcessedCSV
from .forms import CSVUploadForm

# def process_csv(file_path, column_index):
#     pass
    
def process_csv_view(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            column_index = form.cleaned_data['column_to_process']
            processed_files = []

            for csv_file in request.FILES.getlist('csv_files'):
                
                # Use TextIOWrapper to read the content of the uploaded file
                csv_text = TextIOWrapper(csv_file.file, encoding='utf-8')
                df = pd.read_csv(csv_text)
                column_name = df.columns[column_index]
                
                # Process the column and add trailing zeros
                df[column_name].mask( df[column_name].str.isdigit(), df[column_name].str.zfill(10), inplace=True)

                df.column_name = df.column_name.apply('="{}"'.format)
                
                # Write the processed data to a new CSV file
                new_csv_path = os.path.join(settings.MEDIA_ROOT, 'processed', csv_file.name)
                df.to_csv(new_csv_path, index=False)

                # Create a ProcessedCSV object and append it to the list
                processed_csv = ProcessedCSV.objects.create(
                    original_csv=csv_file,
                    processed_csv=new_csv_path
                )
                processed_files.append(processed_csv)

            return render(request, 'processed_csv_list.html', {'processed_files': processed_files})
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})

def download_all_processed_files(request):
    processed_files = ProcessedCSV.objects.all()

    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_zip')
    os.makedirs(temp_dir, exist_ok=True)

    zip_file_path = os.path.join(temp_dir, 'processed_files')

    # Create a temporary directory to store processed files
    temp_processed_dir = os.path.join(temp_dir, 'processed')
    os.makedirs(temp_processed_dir, exist_ok=True)

    # Copy processed files to the temporary directory
    for processed_file in processed_files:
        if processed_file.processed_csv:
            processed_csv_path = os.path.join(settings.MEDIA_ROOT, str(processed_file.processed_csv))
            if os.path.exists(processed_csv_path):
                shutil.copy2(processed_csv_path, temp_processed_dir)

    # Create a zip file from the processed files
    shutil.make_archive(zip_file_path, 'zip', temp_processed_dir)

    # Read the zip file and serve it as an HttpResponse
    with open(f"{zip_file_path}.zip", 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="processed_files.zip"'

    # Clean up temporary files and directories
    shutil.rmtree(temp_dir)

    return response