import requests
import os
from dotenv import load_dotenv

load_dotenv

headers = {
    "apikey": os.getenv("supabase_key"),
    "Authorization": f"Bearer {os.getenv("supabase_key")}",
    "Content-Type": "application/json"
}

def main(target_name: str) -> str:
    # All rows
    # if target_name == "*":
    #     all_rows = get_all_rows()
    #     for entry in all_rows:
    #         total += entry.get("spent")
    #     return f"The total spent is {total}"

    # check if name is in database
    name_response = get_name()
    names: list = []
    for name in name_response:
        names.append(name.get('firstName') + " " + name.get('lastName'))
    # print(names)
    if not(names.__contains__(target_name)):
        return f"Name {target_name} not found in database"
    splitName: list = target_name.split()
    row_response = get_row(splitName[0], splitName[1])
    formatted = format_rows(row_response)
    return formatted
    
def get_name() -> str:
    response = requests.get(
        f"{os.getenv("supabase_url")}/rest/v1/test",
        headers=headers,
        params={"select": "firstName,lastName"}
    )
    return response.json()

def get_row(firstName: str, lastName: str) -> str:
    response = requests.get(
        f"{os.getenv("supabase_url")}/rest/v1/test",
        headers=headers,
        params={"firstName": f"eq.{firstName}",
                "lastName": f"eq.{lastName}"
        }
    )
    return response.json()
def format_rows(rows: list) -> str:
    formatted = []
    for row in rows:
        filtered = {k: v for k, v in row.items() if v is not None}

        row_str = "\n".join(f"{k}: {v}" for k, v in filtered.items())

        formatted.append(row_str)

    return "\n\n".join(formatted)

# def get_spent(name: str) -> str:
#     response = requests.get(
#         f"{os.getenv("supabase_url")}/rest/v1/test",
#         headers=headers,
#         params={    "select": "name,spent",
#                     "name": f"eq.{name}"
#         }
#     )
#     return response.json()

def get_all_rows() -> str:
    response = requests.get(
        f"{os.getenv("supabase_url")}/rest/v1/test",
        headers=headers,
    )
    return response.json()

if __name__ == "__main__":
   print(main("Jamie Abbott"))