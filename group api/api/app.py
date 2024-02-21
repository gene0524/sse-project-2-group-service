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

# TODO: 1. complete the app to return the json format data (group information) based on the queries
app = Flask(__name__)

# Mock database for demonstration purposes
# In a real application, you would query your actual database
groups_info = {
    "group1": {"group_name": "Food Lovers", "members": [{"email": "member1@example.com", "status": "active"}, {"email": "member2@example.com", "status": "pending"}]},
    "group2": {"group_name": "Veggie Friends", "members": [{"email": "member3@example.com", "status": "active"}, {"email": "member4@example.com", "status": "active"}]}
}

@app.route("/", methods=["GET"])
def index():
    # Example: Query parameters could be used to specify which group's information to return
    group_id = request.args.get('group_id', default=None, type=str)
    
    # Check if group_id is provided and valid
    if group_id and group_id in groups_info:
        # Return the requested group's information as JSON
        return jsonify(groups_info[group_id]), 200
    elif group_id:
        # If group_id is provided but not found, return an error message
        return jsonify({"error": "Group not found"}), 404
    else:
        # If no group_id is provided, return information for all groups
        return jsonify(groups_info), 200

########################################
##########       Tables       ##########
########################################
# Group Food List:      group_id    dish_uri    votes_count
# Group Members Info:   group_id    email       status
# Group Registration:   group_id    group_name
# Group Vote:           group_id    dish_uri    email
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

########################################
##########    Create Group    ##########
########################################

# When "create group" button pressed (in main service):
def create_group(group_name, email_list):
    # Create group and retrieve group_id
    _, group_data = add_group_to_groupbase(group_name)
    group_id = group_data[0]['group_id']
    print(group_id)

    # Status: 2 for group owner(first email in list), 1 for member, 0 for pending
    # Assuming the first person in the email list is the group owner
    add_member_to_group(group_id, email_list[0], 2)
    
    # Add other members to Group Members Info, and set their status to pending by default
    for email in email_list[1:]:
        add_member_to_group(group_id, email, 0)

    return

def add_group_to_groupbase(group_name):
    data_to_insert = {
        "group_name": group_name
    }
    data, _ = supabase_client.table("Group Registration").insert([data_to_insert]).execute()
    print(data)
    return data

def add_member_to_group(group_id, email, status):
    data_to_insert = {
        "group_id": group_id,
        "email": email,
        "status": status
    }
    data, _ = supabase_client.table("Group Members Info").insert([data_to_insert]).execute()
    return data

# Sample Usage:
# create_group("group_test_1", ["user1@gmail.com", "user2@gmail.com", "user3@gmail.com"])
# TODO: from client side, check if invited users are already in the User Registration Table

########################################
##########     Group.html     ##########
########################################

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
def print_group_member_info(group_id, width=20):
    """Print group member information in a formatted way."""
    """
    user_FullName = "John Wick"
    print("User1:".ljust(width) + user_FullName)
    print()
    """
    print("Group Members' Full Names:".ljust(width))
    members_data, _ = supabase_client.table("Group Members Info").select("email").eq("group_id", group_id).execute()
    data = members_data[1]
    for index,member in enumerate(data):
        email = member["email"]
        user_data_list, _ = supabase_client.table("User Registration").select("firstname, lastname").eq("email", email).execute()
        user_data = user_data_list[1][0]
        first_name = user_data['firstname']
        last_name = user_data['lastname']
        print(f"User{index}:".ljust(width) + first_name + " " + last_name)

# TODO: 4. Complete the function to return the food list(name & uri) of a group
def print_food_list(group_id, width=20):
    """Print food list information."""
    print()

    food_data,_ = supabase_client.table("Group Food List").select("dish_uri").eq("group_id", group_id).execute()
    print("Group Food List:".ljust(width))
    for food in food_data[1]:
        uri = food['dish_uri']
        # TODO: Fetch the uri to the api to get the food data
        print(uri)


def display_groups(user_email):
    response, _ = supabase_client.table("Group Members Info")\
                    .select("group_id, status, Group Registration (group_name, description)")\
                    .eq("email", user_email)\
                    .execute()
    
    response_list = response[1]
    
    groups = [
        {
            'group_name': group['Group Registration']['group_name'],
            'description': group['Group Registration']['description'],
            'group_id': group['group_id'],
            'status': group['status']
        } for group in response_list
    ]
    print(groups)
    return groups

display_groups("user1@gmail.com")

########################################
##########    Sample Usage    ##########
########################################
