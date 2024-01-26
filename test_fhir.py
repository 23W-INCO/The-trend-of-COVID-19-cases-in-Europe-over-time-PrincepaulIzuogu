import requests
import json

# Replace with the URL of your Flask app
flask_app_url = 'http://127.0.0.1:5000/api/vaccinations'

# FHIR bundle data to send
fhir_bundle_data = [
    {
        "resourceType": "Immunization",
        "id": "1",
        "status": "completed",
        "vaccineCode": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "1119349007"
                }
            ]
        },
        "patient": {
            "reference": "Patient/ALB"
        },
        "occurrenceDateTime": "2022-01-26",
        "doseQuantity": {
            "value": 500.0,
            "unit": "doses"
        },
        "performer": [
            {
                "function": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0443",
                            "code": "AP"
                        }
                    ]
                },
                "actor": {
                    "reference": "Organization/example"
                }
            }
        ]
    },
    {
        "resourceType": "Immunization",
        "id": "2",
        "status": "completed",
        "vaccineCode": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "1119349007"
                }
            ]
        },
        "patient": {
            "reference": "Patient/ALB"
        },
        "occurrenceDateTime": "2022-01-27",
        "doseQuantity": {
            "value": 0,
            "unit": "doses"
        },
        "performer": [
            {
                "function": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0443",
                            "code": "AP"
                        }
                    ]
                },
                "actor": {
                    "reference": "Organization/example"
                }
            }
        ]
    }
]

# Send POST request
response = requests.post(flask_app_url, json=fhir_bundle_data)

# Print the response
print(response.json())
