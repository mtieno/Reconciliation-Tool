import argparse
import csv

def parse_csv(file_path):
    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        return data
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
        exit(1)
    except Exception as e:
        print(f"Error parsing CSV file: {e}")
        exit(1)

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

def generate_report(reconciliation_report, output_path):
    # Extract reconciliation report data
    missing_in_target_count = reconciliation_report['missing_in_target']
    missing_in_source_count = reconciliation_report['missing_in_source']
    discrepancies_count = reconciliation_report['discrepancies']

    # Prepare report data
    report_data = [
        {"Category": "Records missing in target", "Count": missing_in_target_count},
        {"Category": "Records missing in source", "Count": missing_in_source_count},
        {"Category": "Records with field discrepancies", "Count": discrepancies_count}
    ]

    # Write report to CSV file
    fieldnames = ["Category", "Count"]
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_data)

    print(f"Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='CSV Reconciler')
    parser.add_argument('-s', '--source', help='Path to the source CSV file', required=True)
    parser.add_argument('-t', '--target', help='Path to the target CSV file', required=True)
    parser.add_argument('-o', '--output', help='Path to save the output reconciliation report', required=True)
    args = parser.parse_args()

    # Parse source and target CSV files
    source_data = parse_csv(args.source)
    target_data = parse_csv(args.target)

    # Reconcile records
    missing_in_target, missing_in_source, discrepancies = reconcile_records(source_data, target_data)

    # Generate reconciliation report
    reconciliation_report = {
        'missing_in_target': len(missing_in_target),
        'missing_in_source': len(missing_in_source),
        'discrepancies': len(discrepancies)
    }
    generate_report(reconciliation_report, args.output)

    # Print summary
    print("Reconciliation completed:")
    print(f"- Records missing in target: {reconciliation_report['missing_in_target']}")
    print(f"- Records missing in source: {reconciliation_report['missing_in_source']}")
    print(f"- Records with field discrepancies: {reconciliation_report['discrepancies']}")
    print(f"Report saved to: {args.output}")

if __name__ == "__main__":
    main()