from dotenv import load_dotenv
from flask import Flask, jsonify, request
import requests
import supabase
import os

load_dotenv()

# Constants for Supabase URL and API keys
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize the Supabase Client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# TODO: 1. authenticate user for modifying table with Row Level Security
# result = supabase_client.auth.sign_in_with_password({
#     "email": "geneaaaaa@gmail.com",
#     "password": "Team_team2024"}
# )

# TODO: 2. complete the app to return the json format data (group information) based on the queries
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return 
    query = request.args.get("query")
    filter = request.args.get("filter")

    if query and filter:
        try:
            # Query the data from your Supabase table
            data = supabase.table("groupInfo").select("*").execute()
            if data.error:
                raise Exception(data.error.message)
            results = data.data

            # Filter the data based on the query and filter provided
            filtered_data = [i for i in results if query.lower() in str(i.get(filter, '')).lower()]
            return jsonify(filtered_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # If no query and filter provided, return all data
    else:
        data = supabase.table("groupInfo").select("*").execute()
        if data.error:
            return jsonify({"error": data.error.message}), 400
        return jsonify(data.data)


########################################
##########       Tables       ##########
########################################
# Group Food List:      group_id    dish_uri
# Group Members Info:   group_id    email       status
# Group Registration:   group_id    group_name
# User Favorites:       email       dish_uri
# User Registration:    email       first_name  last_name   password


def get_data_from_table(table_name):
    """Fetch data from a Supabase table."""
    # Headers for HTTP requests
    HEADERS = {
        "apikey": SUPABASE_KEY,
        "Authorization": "Bearer " + SUPABASE_KEY,
        "Content-Type": "application/json",
    }
    response = requests.get(f"{SUPABASE_URL}/rest/v1/{table_name}", headers=HEADERS)
    if response.status_code == 200:
        print("Request success!")
        print(response.text)
        return response.json()
    else:
        print(f"Error: {response.text}")
        return f"Error: {response.text}"

def add_group_to_groupbase(group_name):
    data_to_insert = {
        "group_name": group_name
    }
    data, _ = supabase_client.table("Group Registration").insert([data_to_insert]).execute()
    return data

def add_member_to_group(group_id, email):
    data_to_insert = {
        "group_id": group_id,
        "email": email,
        "status": 0
    }
    data, _ = supabase_client.table("Group Members Info").insert([data_to_insert]).execute()
    return data

def add_food_to_group(group_id, dish_uri):
    data_to_insert = {
        "group_id": group_id,
        "dish_uri": dish_uri
    }
    data, _ = supabase_client.table("Group Food List").insert([data_to_insert]).execute()
    return data

def delete_group_from_groupbase(group_id):
    data, _ = supabase_client.table("Group Registration").delete().eq("group_id", group_id).execute()
    return data

def delete_member_from_group(group_id, email):
    data, _ = supabase_client.table("Group Members Info").delete().eq("group_id", group_id).eq("email", email).execute()
    return data

def delete_food_from_group(group_id, dish_uri):
    data, _ = supabase_client.table("Group Members Info").delete().eq("group_id", group_id).eq("dish_uri", dish_uri).execute()
    return data

def return_data(table_name, username):
    """Return data based on username from a Supabase table."""
    data, _ = supabase_client.table(table_name).select("*").eq("username (email)", username).execute()
    return data[1]

def return_user(group_id):
    """Return data based on group_id from a Group Registration table."""
    data, _ = (
        supabase_client.table("Group Registration")
        .select("*")
        .eq("group_id", group_id)
        .execute()
    )
    return data[1]

# TODO: 3. Complete the function to return the full name of the members in a group
def print_group_member_info(user_data, width=20):
    """Print group member information in a formatted way."""
    user_FullName = "John Wick"
    print("User1:".ljust(width) + user_FullName)
    print()

# TODO: 4. Complete the function to return the food list(name & uri) of a group
def print_food_list(favorites_data, width=20):
    """Print food list information."""
    print()


########################################
##########    Sample Usage    ##########
########################################

'''get_data_from_table(table_name)'''
get_data_from_table("User Registration")

'''add_group_to_groupbase(group_name)'''
add_group_to_groupbase("Group1")

# Example usage: 
# favorites_data = return_data("Favorites", username_to_check)
# delete_row_from_table("Favorites", username_to_check, "http://www.edamam.com/ontologies/edamam.owl#recipe_92f5af46a5adafda4b26ff16f4fb7c89")
# print(favorites_data)
# if favorites_data:
#     print("Favorite cuisines:")
#     print_favorites_info(favorites_data)

