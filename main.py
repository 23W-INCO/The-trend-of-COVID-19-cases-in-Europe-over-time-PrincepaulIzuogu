from flask import Flask, request, jsonify, send_file, redirect, url_for
import json
from uuid import uuid4
import os

app = Flask(__name__)


# Path to the processed FHIR bundle data file in the static folder
processed_fhir_file_path = os.path.join(app.root_path, 'static', 'processed_fhir.json')

# Global variable to store processed FHIR bundle data
processed_fhir_data = []

def validate_immunization(resource):
    # Simple validation: Check if required fields are present
    required_fields = ['resourceType', 'status', 'vaccineCode', 'patient', 'occurrenceDateTime', 'doseQuantity', 'performer']
    for field in required_fields:
        if field not in resource:
            return False
    return True

@app.route('/api/vaccinations', methods=['POST'])
def receive_fhir_bundle():
    try:
        # Assuming the incoming data is a list of Immunization resources
        data = request.get_json()

        # Validate and process each Immunization resource
        for resource in data:
            if validate_immunization(resource):
                # Process the data (example: print the received data)
                print("Received Immunization data:", resource)

                # Append the valid data to the global variable
                processed_fhir_data.append(resource)
            else:
                return jsonify({'status': 'error', 'message': 'Invalid Immunization resource'})

        # Store the valid data in the file in the static folder
        with open(processed_fhir_file_path, 'w') as file:
            json.dump(processed_fhir_data, file, indent=2)

        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/vaccinations', methods=['GET'])
def get_fhir_bundle():
    try:
        # Return the stored processed FHIR bundle data
        return jsonify(processed_fhir_data)

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

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
@app.route('/extra_fields.json')
def get_processed_fhir():
    return send_file('static/processed_fhir.json')

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


