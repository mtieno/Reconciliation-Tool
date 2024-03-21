from django.shortcuts import render

import csv
from django.shortcuts import render
from .forms import CSVUploadForm
from .models import CSVRecord

def parse_csv(file):
    data = []
    reader = csv.reader(file)
    header = next(reader)  # Get the header
    for row in reader:
        record = {}
        for i, value in enumerate(row):
            record[header[i]] = value.strip()  # Store each field in the record
        data.append(record)
    return data

def reconcile_records(source_data, target_data):
    # Implement the reconciliation logic
    pass

def home(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            source_data = parse_csv(request.FILES['source_file'])
            target_data = parse_csv(request.FILES['target_file'])
            # Reconcile records
            # Generate HTML report
            # Return HTML response
    else:
        form = CSVUploadForm()
    return render(request, 'home.html', {'form': form})
