import csv
from django import forms
from django.core.exceptions import ValidationError

class CSVUploadForm(forms.Form):
    source_file = forms.FileField(label='Source CSV File')
    target_file = forms.FileField(label='Target CSV File')

    def _validate_csv_format(self, file):
        try:
            dialect = csv.Sniffer().sniff(file.read(1024).decode('utf-8'))
            file.seek(0)
            csv.reader(file, dialect)
        except csv.Error:
            raise ValidationError("Invalid CSV format. Please ensure the file is a valid CSV.")

    def clean_source_file(self):
        source_file = self.cleaned_data['source_file']
        self._validate_csv_format(source_file)
        return source_file

    def clean_target_file(self):
        target_file = self.cleaned_data['target_file']
        self._validate_csv_format(target_file)
        return target_file