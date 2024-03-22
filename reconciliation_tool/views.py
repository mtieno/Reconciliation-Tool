import csv
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .forms import CSVUploadForm
from .models import CSVRecord

from django.http import HttpResponseBadRequest

def parse_csv(file):
    try:
        data = []
        reader = csv.DictReader(file.read().decode('utf-8').splitlines(), delimiter=',')
        for row in reader:
            data.append(row)
        return data
    except UnicodeDecodeError as e:
        raise HttpResponseBadRequest("Error parsing CSV file: {}".format(str(e)))
    except csv.Error as e:
        raise HttpResponseBadRequest("CSV parsing error: {}".format(str(e)))
    
def reconcile_records(source_data, target_data):
    # Convert data to dictionaries with unique identifiers as keys
    source_dict = {record['ID']: record for record in source_data}
    target_dict = {record['ID']: record for record in target_data}

    # Find missing records
    missing_in_target = [record for identifier, record in source_dict.items() if identifier not in target_dict]
    missing_in_source = [record for identifier, record in target_dict.items() if identifier not in source_dict]

    # Find discrepancies
    discrepancies = []
    for identifier, source_record in source_dict.items():
        if identifier in target_dict:
            target_record = target_dict[identifier]
            for key, source_value in source_record.items():
                target_value = target_record.get(key)
                if target_value != source_value:
                    discrepancies.append({
                        'identifier': identifier,
                        'field': key,
                        'source_value': source_value,
                        'target_value': target_value
                    })

    return missing_in_target, missing_in_source, discrepancies

def home(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                source_data = parse_csv(request.FILES['source_file'])
                target_data = parse_csv(request.FILES['target_file'])
                # Generate and return reconciliation report
                missing_in_target, missing_in_source, discrepancies = reconcile_records(source_data, target_data)
                return render(request, 'report.html', {
                    'missing_in_target': missing_in_target,
                    'missing_in_source': missing_in_source,
                    'discrepancies': discrepancies
                })
            except Exception as e:
                return HttpResponseBadRequest(str(e))  # Return a generic error response
    else:
        form = CSVUploadForm()
    return render(request, 'home.html', {'form': form})