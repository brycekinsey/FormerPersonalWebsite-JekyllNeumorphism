import os
import json
import sys
from dotenv import load_dotenv
import os.path
from linkedin_api import Linkedin

# Specify the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
# Load the .env file
load_dotenv(dotenv_path)

try:
    # Fetch LinkedIn username, password, and public ID from environment variables
    linkedin_username = os.environ.get('LINKEDIN_USERNAME')
    linkedin_password = os.environ.get('LINKEDIN_PASSWORD')
    linkedin_public_id = os.environ.get('LINKEDIN_PUBLIC_ID')
    
    if not all([linkedin_username, linkedin_password, linkedin_public_id]):
        raise ValueError("Missing LinkedIn credentials or public ID.")

    # Authenticate with LinkedIn
    try:
        api = Linkedin(linkedin_username, linkedin_password)
    except Exception as auth_error:
        raise ValueError(f"LinkedIn authentication failed: {auth_error}")

    # Fetch LinkedIn profile information
    try:
        linkedin_profile = api.get_profile(public_id=linkedin_public_id)
    except Exception as fetch_error:
        raise ValueError(f"Failed to fetch LinkedIn profile: {fetch_error}")

    # keys to be removed based on location values
    keys_to_remove = []

    if 'birthDate' in linkedin_profile:
            keys_to_remove.append('birthDate')
    if 'geoLocation' in linkedin_profile:
        if 'postalCode' in linkedin_profile['geoLocation']:
            keys_to_remove.append('geoLocation')
    if 'geoLocationName' in linkedin_profile:
            keys_to_remove.append('geoLocationName')
    if 'location' in linkedin_profile:
        if 'basicLocation' in linkedin_profile['location']:
            if 'postalCode' in linkedin_profile['location']['basicLocation']:
                keys_to_remove.append('location')

    # Remove the keys
    for key in keys_to_remove:
        linkedin_profile.pop(key, None)

    # Save LinkedIn profile information to JSON file
    try:
        with open('_data/linkedin_profile.json', 'w') as f:
            json.dump(linkedin_profile, f)
    except Exception as file_error:
        raise ValueError(f"Failed to write to JSON file: {file_error}")

except ValueError as ve:
    print(ve)
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)