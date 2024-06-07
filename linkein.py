import json
import os
from linkedin_api import Linkedin

# Set your LinkedIn credentials as environment variables for security
linkedin_email = os.getenv('LINKEDIN_EMAIL', 'joshcalvin030@gmail.com')
linkedin_password = os.getenv('LINKEDIN_PASSWORD', 'Joshua@2022')

# Authenticate using any LinkedIn account credentials
try:
    api = Linkedin(linkedin_email, linkedin_password)
except Exception as e:
    print(f"Error during authentication: {e}")
    exit(1)

# Define the university name and keyword
university_name = "Imperial College London"
keyword = "chess"

# Perform the search operation
try:
    search_results = api.search_people(
        keywords=f"{university_name} {keyword}",  # Search by both university name and keyword
        limit=10  # Limiting to 10 results, adjust as needed
    )

    if not search_results:
        print("No search results found.")
        exit(1)

    # Check each profile for the keyword "chess" and the university name in education
    for person in search_results:
        profile_id = person['urn_id']
        profile_info = api.get_profile(profile_id)

        # Convert profile_info to a string and check if "chess" is present
        profile_info_str = json.dumps(profile_info).lower()
        keyword_present = keyword.lower() in profile_info_str

        # Check if the university name is in the education field
        education = profile_info.get('education', [])
        university_present = any(university_name.lower() in (edu.get('schoolName', '').lower() or '') for edu in education)

        if keyword_present and university_present:
            print(f"Name: {person['name']}")
            print(f"Profile Info: {json.dumps(profile_info, indent=2)}")
    
except Exception as e:
    print(f"Error during search or fetching profile info: {e}")
