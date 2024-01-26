from flask import Flask, request, jsonify, send_file, redirect, url_for
import json
from uuid import uuid4

app = Flask(__name__)

# Existing data (if any)
existing_data = []

@app.route('/api/vaccinations', methods=['POST'])
def receive_fhir_bundles():
    try:
        fhir_bundles = request.json  # Assuming the FHIR Bundles are sent as JSON
        print("Received FHIR Bundles:", json.dumps(fhir_bundles, indent=2))

        # Extract and convert FHIR Bundles to JSON
        extracted_data, extra_fields_data = extract_and_convert(fhir_bundles)
        print("Extracted Data:", json.dumps(extracted_data, indent=2))

        # Check for duplicates and mismatch before storing
        check_for_duplicates(extracted_data)
        check_for_mismatch(extracted_data)

        # Store the extracted data in static/data.json
        save_to_data_json(extracted_data)

        # Store extra fields in a separate file
        save_extra_fields_to_file(extra_fields_data)

        return redirect(url_for('success'))
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/api/get_data', methods=['GET'])
def get_vaccination_data():
    try:
        with open('static/data.json', 'r') as file:
            existing_vaccination_data = json.load(file)
    except FileNotFoundError:
        return jsonify({'error': 'data.json not found'}), 404

    return jsonify(existing_vaccination_data), 200


@app.route('/success')
def success():
    return jsonify({"message": "FHIR Bundles received and processed successfully"}), 200

def extract_and_convert(fhir_bundles):
    extracted_data = []
    extra_fields_data = []  # List to store entries with extra fields

    for fhir_bundle in fhir_bundles:
        entries = fhir_bundle.get("entry", [])

        for entry in entries:
            if "resource" in entry:
                immunization_resource = entry["resource"]

                # Extract relevant fields
                extracted_entry = {
                    "iso_code": immunization_resource["extension"][0]["valueString"],
                    "date": immunization_resource["occurrenceDateTime"],
                    "continent": immunization_resource["extension"][1]["valueString"],
                    "location": immunization_resource["extension"][2]["valueString"],
                    "total_cases": immunization_resource["extension"][3]["valueDecimal"],
                    "population": immunization_resource["extension"][4]["valueInteger"],
                    "total_vaccinations": immunization_resource["extension"][5]["valueInteger"],
                    "people_vaccinated": immunization_resource["extension"][6]["valueInteger"]
                }
                extracted_data.append(extracted_entry)

                # Extract extra fields
                extra_fields_entry = {
                    "extra_fields": {
                        key: immunization_resource[key] for key in immunization_resource if key not in extracted_entry
                    }
                }
                extra_fields_data.append(extra_fields_entry)

    return extracted_data, extra_fields_data

def save_extra_fields_to_file(extra_fields_data):
    with open('static/extra_fields.json', 'w') as extra_fields_file:
        json.dump(extra_fields_data, extra_fields_file, indent=2)

def save_to_data_json(data):
    existing_data.extend(data)
    with open('static/data.json', 'w') as data_file:
        json.dump(existing_data, data_file, indent=2)


# Route for serving index.html
@app.route('/')
def index():
    return send_file('templates/index.html')

# Route for serving script.js
@app.route('/script.js')
def get_script():
    return send_file('static/script.js')

# Route for serving dough.js
@app.route('/dough.js')
def get_dough_script():
    return send_file('static/dough.js')

# Route for serving styles.css
@app.route('/styles.css')
def get_styles():
    return send_file('static/styles.css')

# Route for serving data.json
@app.route('/data.json')
def get_data():
    return send_file('static/data.json')

# Route for serving flags from the root directory
@app.route('/flags/<filename>')
def get_flag(filename):
    return send_file(f'flags/{filename}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
