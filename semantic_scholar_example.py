import requests
import re
format_doi = lambda url: f"doi:{re.sub(r'https://doi\.org/', '', url)}"
paperId = "649def34f8be52c8b66281af98ae884c09aef38b"
paperId = "https://doi.org/10.1016/j.cma.2007.07.016"
# Define the API endpoint URL
url = f"http://api.semanticscholar.org/graph/v1/paper/{format_doi(paperId)}"
print(format_doi(paperId))
#url = f"http://api.semanticscholar.org/graph/v1/paper/{paperId}"

# Define the query parameters
query_params = {"fields": "title,url,publicationDate,abstract,openAccessPdf,citationStyles"}

# Directly define the API key (Reminder: Securely handle API keys in production environments)
api_key = "Hg3W2wCtsEyjvsc5cdJi8QyjcBTgyrh8aXkQ3QPe"

# Define headers with API key
headers = {"x-api-key": api_key}

# Send the API request
response = requests.get(url, params=query_params)

# Check response status
if response.status_code == 200:
   response_data = response.json()
   # Process and print the response data as needed
   print(response_data)
else:
   print(f"Request failed with status code {response.status_code}: {response.text}")