import requests
import json

# Example FHIR Bundles
fhir_bundles = [
    {
        "resourceType": "Immunization",
        "id": "ce655d9a-5986-40cb-93e3-728856fb3d61",
        "status": "completed",
        "vaccineCode": {"coding": [{"system": "http://snomed.info/sct", "code": "1119349007"}]},
        "patient": {"reference": "Patient/ALB"},
        "occurrenceDateTime": "2021-01-13",
        "doseQuantity": {"value": 188.0, "unit": "doses"},
        "performer": [
            {
                "function": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0443", "code": "AP"}]},
                "actor": {"reference": "Organization/example"}
            }
        ]
    },
    {
        "resourceType": "Immunization",
        "id": "f61e26b8-177a-4aad-89d6-05fba2af6a55",
        "status": "completed",
        "vaccineCode": {"coding": [{"system": "http://snomed.info/sct", "code": "1119349007"}]},
        "patient": {"reference": "Patient/ALB"},
        "occurrenceDateTime": "2021-01-14",
        "doseQuantity": {"value": 266.0, "unit": "doses"},
        "performer": [
            {
                "function": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0443", "code": "AP"}]},
                "actor": {"reference": "Organization/example"}
            }
        ]
    }
    # Add more Immunization entries as needed
]

# Function to send FHIR Bundles to the Flask app
def send_fhir_bundles(fhir_bundles):
    try:
        send_data_to_flask_app(fhir_bundles)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def send_data_to_flask_app(data):
    url = "http://localhost:5000/api/vaccinations"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Data sent successfully.")
    else:
        print(f"Error sending data. Status Code: {response.status_code}, Content: {response.content}")

# Send FHIR Bundles to the Flask app without processing
success = send_fhir_bundles(fhir_bundles)

if success:
    print("FHIR Bundles sent successfully.")
else:
    print("Error sending FHIR Bundles.")
