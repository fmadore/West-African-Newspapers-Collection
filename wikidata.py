import requests
import pandas as pd

# Define the SPARQL query to fetch the required data
query = """
SELECT ?item ?itemLabel ?inception ?title ?website ?lccn ?oclc ?zdb ?bnf WHERE {
  ?item wdt:P31 wd:Q11032;
        wdt:P495 wd:Q1008.
  OPTIONAL { ?item wdt:P571 ?inception. }
  OPTIONAL { ?item wdt:P1476 ?title. }
  OPTIONAL { ?item wdt:P856 ?website. }
  OPTIONAL { ?item wdt:P1144 ?lccn. }
  OPTIONAL { ?item wdt:P243 ?oclc. }
  OPTIONAL { ?item wdt:P1042 ?zdb. }
  OPTIONAL { ?item wdt:P268 ?bnf. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""


# Function to execute the SPARQL query
def execute_sparql_query(query):
    url = "https://query.wikidata.org/sparql"
    headers = {
        'User-Agent': 'Wikidata Python Client/1.0 (https://www.wikidata.org/wiki/User:YourUsername)'
    }
    response = requests.get(url, params={'query': query, 'format': 'json'}, headers=headers)
    data = response.json()
    return data


# Fetch the data
data = execute_sparql_query(query)

# Parse the results
results = data['results']['bindings']

# Prepare the data for the DataFrame
parsed_data = []
seen_qids = set()

for result in results:
    item = result.get('item', {}).get('value', '')

    if item in seen_qids:
        continue

    seen_qids.add(item)

    inception = result.get('inception', {}).get('value', '')
    if inception and len(inception) > 10:  # Full date format with time
        inception = inception[:10]  # Keep only YYYY-MM-DD
    elif inception and len(inception) == 10:  # Full date format without time
        inception = inception  # Keep as is
    elif inception and len(inception) == 7:  # Year and month format
        inception = inception  # Keep as is
    elif inception and len(inception) == 4:  # Year format
        inception = inception  # Keep as is

    title = result.get('title', {}).get('value', '')
    website = result.get('website', {}).get('value', '')

    lccn = result.get('lccn', {}).get('value', '')
    if lccn:
        lccn = f"https://lccn.loc.gov/{lccn}"

    oclc = result.get('oclc', {}).get('value', '')
    if oclc:
        oclc = f"https://www.worldcat.org/oclc/{oclc}"

    zdb = result.get('zdb', {}).get('value', '')
    if zdb:
        zdb = f"https://ld.zdb-services.de/resource/zbmed/{zdb}"

    bnf = result.get('bnf', {}).get('value', '')
    if bnf:
        bnf = f"https://catalogue.bnf.fr/ark:/12148/cb{bnf}"

    parsed_data.append({
        'QID': item,
        'Title': title,
        'Inception': inception,
        'Website': website,
        'LCCN': lccn,
        'OCLC': oclc,
        'ZDB': zdb,
        'BnF ID': bnf
    })

# Create a DataFrame
df = pd.DataFrame(parsed_data)

# Save to CSV
df.to_csv('wikidata_entries.csv', index=False)

print("Data saved to wikidata_entries.csv")
