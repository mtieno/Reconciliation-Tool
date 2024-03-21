from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from reconciliation_tool.forms import CSVUploadForm
from reconciliation_tool.views import reconcile_records, parse_csv


class CSVUploadFormTests(TestCase):
   def test_valid_form(self):
    # Test case for a valid form submission
    file_data = {
        'source_file': SimpleUploadedFile("source.csv", b"csv_content"),
        'target_file': SimpleUploadedFile("target.csv", b"csv_content")
    }
    form = CSVUploadForm(data={}, files=file_data)
    self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_form(self):
        # Test case for an invalid form submission
        form = CSVUploadForm(data={})
        self.assertTrue(form.is_valid(), form.errors)

class CSVProcessingTests(TestCase):
    def test_parse_csv(self):
        # Test case for parsing source CSV file
        source_csv_content = b"ID,Name,Date,Amount\n001,John Doe,2023-01-01,100.00\n002,Jane Smith,2023-01-02,200.50\n003,Robert Brown,2023-01-03,300.75"
        source_csv_file = SimpleUploadedFile("source.csv", source_csv_content)
        parsed_source_data = parse_csv(source_csv_file)
        expected_source_data = [
            {'ID': '001', 'Name': 'John Doe', 'Date': '2023-01-01', 'Amount': '100.00'},
            {'ID': '002', 'Name': 'Jane Smith', 'Date': '2023-01-02', 'Amount': '200.50'},
            {'ID': '003', 'Name': 'Robert Brown', 'Date': '2023-01-03', 'Amount': '300.75'}
        ]
        self.assertEqual(parsed_source_data, expected_source_data)

        # Test case for parsing target CSV file
        target_csv_content = b"ID,Name,Date,Amount\n001,John Doe,2023-01-01,100.00\n002,Jane Smith,2023-01-04,200.50\n004,Emily White,2023-01-05,400.90"
        target_csv_file = SimpleUploadedFile("target.csv", target_csv_content)
        parsed_target_data = parse_csv(target_csv_file)
        expected_target_data = [
            {'ID': '001', 'Name': 'John Doe', 'Date': '2023-01-01', 'Amount': '100.00'},
            {'ID': '002', 'Name': 'Jane Smith', 'Date': '2023-01-04', 'Amount': '200.50'},
            {'ID': '004', 'Name': 'Emily White', 'Date': '2023-01-05', 'Amount': '400.90'}
        ]
        self.assertEqual(parsed_target_data, expected_target_data)

    def test_reconciliation(self):
        # Test case for data reconciliation
        source_data = [
            {'ID': '001', 'Name': 'John Doe', 'Date': '2023-01-01', 'Amount': '100.00'},
            {'ID': '002', 'Name': 'Jane Smith', 'Date': '2023-01-02', 'Amount': '200.50'},
            {'ID': '003', 'Name': 'Robert Brown', 'Date': '2023-01-03', 'Amount': '300.75'}
        ]
        target_data = [
            {'ID': '001', 'Name': 'John Doe', 'Date': '2023-01-01', 'Amount': '100.00'},
            {'ID': '002', 'Name': 'Jane Smith', 'Date': '2023-01-04', 'Amount': '200.50'},
            {'ID': '004', 'Name': 'Emily White', 'Date': '2023-01-05', 'Amount': '400.90'}
        ]
        missing_in_target, missing_in_source, discrepancies = reconcile_records(source_data, target_data)
        # Asserting the results of reconciliation
        self.assertEqual(missing_in_target, [{'ID': '003', 'Name': 'Robert Brown', 'Date': '2023-01-03', 'Amount': '300.75'}])
        self.assertEqual(missing_in_source, [])
        self.assertEqual(discrepancies, [])