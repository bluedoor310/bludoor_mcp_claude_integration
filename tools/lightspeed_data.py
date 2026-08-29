import requests
import os
from dotenv import load_dotenv

load_dotenv() 

headers = {
    "Authorization": f"Bearer {os.getenv("airtable_key")}"
}

STATE_MAP = {
    "AL": "AL", "ALABAMA": "AL",
    "AK": "AK", "ALASKA": "AK",
    "AZ": "AZ", "ARIZONA": "AZ",
    "AR": "AR", "ARKANSAS": "AR",
    "CA": "CA", "CALIFORNIA": "CA",
    "CO": "CO", "COLORADO": "CO",
    "CT": "CT", "CONNECTICUT": "CT",
    "DE": "DE", "DELAWARE": "DE",
    "FL": "FL", "FLORIDA": "FL",
    "GA": "GA", "GEORGIA": "GA",
    "HI": "HI", "HAWAII": "HI",
    "ID": "ID", "IDAHO": "ID",
    "IL": "IL", "ILLINOIS": "IL",
    "IN": "IN", "INDIANA": "IN",
    "IA": "IA", "IOWA": "IA",
    "KS": "KS", "KANSAS": "KS",
    "KY": "KY", "KENTUCKY": "KY",
    "LA": "LA", "LOUISIANA": "LA",
    "ME": "ME", "MAINE": "ME",
    "MD": "MD", "MARYLAND": "MD",
    "MA": "MA", "MASSACHUSETTS": "MA",
    "MI": "MI", "MICHIGAN": "MI",
    "MN": "MN", "MINNESOTA": "MN",
    "MS": "MS", "MISSISSIPPI": "MS",
    "MO": "MO", "MISSOURI": "MO",
    "MT": "MT", "MONTANA": "MT",
    "NE": "NE", "NEBRASKA": "NE",
    "NV": "NV", "NEVADA": "NV",
    "NH": "NH", "NEW HAMPSHIRE": "NH",
    "NJ": "NJ", "NEW JERSEY": "NJ",
    "NM": "NM", "NEW MEXICO": "NM",
    "NY": "NY", "NEW YORK": "NY",
    "NC": "NC", "NORTH CAROLINA": "NC",
    "ND": "ND", "NORTH DAKOTA": "ND",
    "OH": "OH", "OHIO": "OH",
    "OK": "OK", "OKLAHOMA": "OK",
    "OR": "OR", "OREGON": "OR",
    "PA": "PA", "PENNSYLVANIA": "PA",
    "RI": "RI", "RHODE ISLAND": "RI",
    "SC": "SC", "SOUTH CAROLINA": "SC",
    "SD": "SD", "SOUTH DAKOTA": "SD",
    "TN": "TN", "TENNESSEE": "TN",
    "TX": "TX", "TEXAS": "TX",
    "UT": "UT", "UTAH": "UT",
    "VT": "VT", "VERMONT": "VT",
    "VA": "VA", "VIRGINIA": "VA",
    "WA": "WA", "WASHINGTON": "WA",
    "WV": "WV", "WEST VIRGINIA": "WV",
    "WI": "WI", "WISCONSIN": "WI",
    "WY": "WY", "WYOMING": "WY",
}

def main(target_name: str) -> str:
    # all data
    if target_name == "*":
        all_response = get_all()
        formatted_table = format_rows(all_response)
        return formatted_table
    # search by location
    elif target_name.startswith("location"):
        zip_code, city, state = parse_location(target_name)
        print("ZIP:", zip_code)
        print("CITY:", city)
        print("STATE:", state)
        location_response = get_row_by_location(zip_code, city, state)
        print(location_response)
        formatted_table = format_rows(location_response)
        return formatted_table
    # search by name
    else:
        name_response = get_names()
        names: list = []
        for record in name_response["records"]:
            fields = record.get("fields", {})
            first = fields.get("firstName", "")
            last = fields.get("lastName", "")
            names.append(f"{first} {last}")
        if not(names.__contains__(target_name)):
            return f"Name {target_name} not found in database"
        splitName: list = target_name.split()
        row_response = get_row_by_name(splitName[0], splitName[1])
        formatted_table = format_rows(row_response)
        return formatted_table 

# return json response of first names and last names  
def get_names() -> str:
    response = requests.get(
        f"{os.getenv("airtable_url")}/integrationTest?fields[]=firstName&fields[]=lastName",
        headers=headers
    )
    return response.json()
# return all the data in airtable
def get_all() -> str:
    response = requests.get(
        f"{os.getenv("airtable_url")}/integrationTest",
        headers=headers
    )
    return response.json()
# search for a row by name
def get_row_by_name(first: str, last: str) -> str:
    response = requests.get(
        f"{os.getenv("airtable_url")}/integrationTest?filterByFormula=AND( \
            {{firstName}}='{first}', \
            {{lastName}}='{last}' \
        )",
        headers=headers
    )
    return response.json()

# search for row by zipcode, city and state
# def get_row_by_location(zip: int, city: str, state: str) -> str: 
#     formula = f"AND({{address.zipCode}}='{zip}',{{address.city}}='{city}',{{address.state}}='{state}')"
#     response = requests.get(
#         f"{os.getenv("airtable_url")}/integrationTest",
#         headers=headers,
#         params={"filterByFormula": formula}
#     )
#     return response.json()
def get_row_by_location(zip: int = None, city: str = None, state: str = None) -> str:
    conditions = []
    if zip:
        conditions.append(f"{{address.zipCode}}='{zip}'")
    if city:
        conditions.append(f"{{address.city}}='{city}'")
    if state:
        conditions.append(f"{{address.state}}='{state}'")

    if not conditions:
        # no location info provided at all
        return {"records": []}

    if len(conditions) == 1:
        formula = conditions[0]
    else:
        formula = f"AND({','.join(conditions)})"

    response = requests.get(
        f"{os.getenv("airtable_url")}/integrationTest",
        headers=headers,
        params={"filterByFormula": formula}
    )
    return response.json()

# formats the data returned by search row by name
def format_rows(rows: list) -> str:
    formatted_table = []
    for row in rows["records"]:
        formatted_row = []
        fields = row.get("fields", {})
        for key, value in fields.items():
            formatted_row.append(f"{key}: {value}")
        
        formatted_table.append(formatted_row)
    
    return formatted_table

# def parse_location(target_name: str) -> str:
#     parts = target_name.split()[1:]
#     parts = [p for p in parts if p != "-"]

#     zip_code = None
#     city = None
#     state = None

#     # ZIP
#     if parts and parts[0].isdigit():
#         zip_code = parts.pop(0)

#     # STATE (longest match from end)
#     for i in range(len(parts), 0, -1):
#         candidate = " ".join(parts[i-1:]).upper()
#         if candidate in STATE_MAP:
#             state = STATE_MAP[candidate]  # <-- normalize here
#             parts = parts[:i-1]
#             break

#     # CITY
#     if parts:
#         city = " ".join(parts)

#     return zip_code, city, state
def parse_location(target_name: str) -> str:
    parts = target_name.split()[1:]
    parts = [p for p in parts if p != "-"]

    zip_code = None
    city = None
    state = None

    # ZIP (optional)
    if parts and parts[0].isdigit():
        zip_code = parts.pop(0)

    # STATE (optional, longest match from end)
    for i in range(len(parts), 0, -1):
        candidate = " ".join(parts[i-1:]).upper()
        if candidate in STATE_MAP:
            state = STATE_MAP[candidate]
            parts = parts[:i-1]
            break

    # CITY (optional, whatever's left)
    if parts:
        city = " ".join(parts)

    return zip_code, city, state

if __name__ == "__main__":
   print(main("location 07055 Passaic NJ"))