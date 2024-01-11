from flask import Flask, send_file, jsonify, Response
from apiflask import APIFlask
import json

app = APIFlask(__name__, spec_path='/openapi.yaml')
app.config['SPEC_FORMAT'] = 'yaml'

# Function to convert existing vaccination data to FHIR Immunization resource
def convert_to_fhir_vaccination(existing_vaccination_data):
    for vaccination_record in existing_vaccination_data:
        fhir_immunization = {
            "resourceType": "Immunization",
            "status": "completed",
            "occurrenceDateTime": vaccination_record.get("date", ""),
            "vaccineCode": {
                "text": f"COVID-19 Vaccine ({vaccination_record.get('total_vaccinations', 0)})"
            },
            "patient": {
                "reference": f"Location/{vaccination_record.get('iso_code', '')}"
            },
            "doseQuantity": {
                "value": vaccination_record.get('total_vaccinations', 0),
                "unit": "doses"
            },
            "note": [
                {"text": f"Location: {vaccination_record.get('location', '')}"},
                {"text": f"Continent: {vaccination_record.get('continent', '')}"},
                {"text": f"Total Cases: {vaccination_record.get('total_cases', 0)}"},
                {"text": f"Population: {vaccination_record.get('population', 0)}"},
                {"text": f"People Vaccinated: {vaccination_record.get('people_vaccinated', 0)}"},
                {"text": f"People Fully Vaccinated: {vaccination_record.get('people_fully_vaccinated', 0)}"},
                {"text": f"Total Vaccinations Per Hundred: {vaccination_record.get('total_vaccinations_per_hundred', 0)}"},
                {"text": f"People Vaccinated Per Hundred: {vaccination_record.get('people_vaccinated_per_hundred', 0)}"},
                {"text": f"People Fully Vaccinated Per Hundred: {vaccination_record.get('people_fully_vaccinated_per_hundred', 0)}"}
            ]
        }
        yield json.dumps(fhir_immunization) + '\n'

# Route for serving FHIR-formatted vaccination data (GET request)
@app.route('/api/vaccinations', methods=['GET'])
def get_vaccination_data():
    try:
        with open('static/data.json', 'r') as file:
            existing_vaccination_data = json.load(file)
    except FileNotFoundError:
        return jsonify({'error': 'data.json not found'}), 404

    fhir_vaccination_data = list(convert_to_fhir_vaccination(existing_vaccination_data))

    # Return the streamed FHIR-formatted vaccination data in the API response
    return Response(fhir_vaccination_data, content_type='text/plain'), 200

# Route for posting vaccination data in FHIR format (POST request)
@app.route('/api/vaccinations', methods=['POST'])
def post_vaccination_data():
    try:
        # Load existing vaccination data from data.json
        with open('static/data.json', 'r') as file:
            existing_vaccination_data = json.load(file)

        # Get the posted data from the request
        posted_data = request.get_json()

        # Assuming posted_data is a list of new vaccination records
        # Convert new data to FHIR format and extend existing data
        updated_data = list(convert_to_fhir_vaccination(posted_data))
        existing_vaccination_data.extend(updated_data)

        # Stream the FHIR-formatted vaccination data directly in the API response
        def generate_fhir_vaccination_data():
            for fhir_vaccination_record in updated_data:
                yield json.dumps(fhir_vaccination_record) + '\n'

        # Return the streamed FHIR-formatted vaccination data in the API response
        return Response(generate_fhir_vaccination_data(), content_type='text/plain'), 200

    except FileNotFoundError:
        return jsonify({'error': 'data.json not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error processing the request: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
