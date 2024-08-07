import math
import os

import pandas as pd

from utils.hubspot import hubSpotIntegration as hubSpot

# Read CSV file
csv_file_path = os.getcwd() + '/files/Beneficiary_Data_Test_File.csv'
print(csv_file_path)
data = pd.read_csv(csv_file_path)

# Display the first few rows of the dataframe to check
print(data.head())

# Create the properties
for property_data in hubSpot.properties:
    response = hubSpot.create_property(property_data)
    print(response)


# Function to convert percentage strings to integers
def convert_percentage(percentage):
    if isinstance(percentage, str):
        return int(percentage.strip('%'))
    return 0


# Function to sanitize data for JSON
def sanitize_value(value):
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return 0
    return value if value is not None else ""


# Convert records to HubSpot contact format
hubspot_contacts = []
for index, row in data.iterrows():
    contact = {"properties": []}

    if 'Policyholder Name' in row:
        contact["properties"].append(
            {"property": "policyholder_name", "value": sanitize_value(row['Policyholder Name'])})
        contact["properties"].append(
            {"property": "firstName", "value": sanitize_value(row['Policyholder Name'])})
    if 'Policy Number' in row:
        contact["properties"].append({"property": "policy_number", "value": sanitize_value(row['Policy Number'])})

    if 'Beneficiary 1' in row:
        contact["properties"].append({"property": "beneficiary_1", "value": sanitize_value(row['Beneficiary 1'])})
    if 'Beneficiary 2' in row:
        contact["properties"].append({"property": "beneficiary_2", "value": sanitize_value(row['Beneficiary 2'])})
    if 'Beneficiary 3' in row:
        contact["properties"].append({"property": "beneficiary_3", "value": sanitize_value(row['Beneficiary 3'])})
    if 'Beneficiary 1 %' in row:
        contact["properties"].append(
            {"property": "beneficiary_1_percent", "value": sanitize_value(convert_percentage(row['Beneficiary 1 %']))})
    if 'Beneficiary 2 %' in row:
        contact["properties"].append(
            {"property": "beneficiary_2_percent", "value": sanitize_value(convert_percentage(row['Beneficiary 2 %']))})
    if 'Beneficiary 3 %' in row:
        contact["properties"].append(
            {"property": "beneficiary_3_percent", "value": sanitize_value(convert_percentage(row['Beneficiary 3 %']))})
    if 'phone_number' in row:
        contact["properties"].append(
            {"property": "phone_number_property", "value": sanitize_value(row['phone_number'])})
    if 'last_call_topic' in row:
        contact["properties"].append({"property": "last_call_topic", "value": sanitize_value(row['last_call_topic'])})
    if 'last_call_status' in row:
        contact["properties"].append({"property": "last_call_status", "value": sanitize_value(row['last_call_status'])})
    if 'email' in row:
        contact["properties"].append({"property": "email", "value": sanitize_value(row['email'])})

    hubspot_contacts.append(contact)

# Assuming hubspot.create_contact is a function that sends data to HubSpot
for contact in hubspot_contacts:
    response = hubSpot.create_contact(contact)
    print(response)
