from dotenv import load_dotenv
from flask import Flask, jsonify, request
import requests
import supabase
import os

load_dotenv()

# Constants for Supabase UasdfRL and API keys
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
        # print("Request success!")
        print(response.text)
        return response.json()
    else:
        # print(f"Error: {response.text}")
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

    # Assuming the first person in the email list is the group owner (status 2)
    add_member_to_group(group_id, email_list[0], 2)
    # Add other members to Group Members Info, and set their status to pending (status 0) by default
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
##########    Voting.html     ##########
########################################
def display_vote_options(group_id, user_email):
    response_1, _ = supabase_client.table("Group Food List")\
                    .select("dish_uri, votes_count")\
                    .eq("group_id", group_id)\
                    .execute()
    
    dish_list = response_1[1]
    
    response_2, _ = supabase_client.table("Group Vote")\
                    .select("dish_uri")\
                    .eq("group_id", group_id).eq("email", user_email)\
                    .execute()

    options_voted = response_2[1]
    
    # Create a list of dish_uris that the user has voted for
    voted_list = [vote['dish_uri'] for vote in options_voted]  
    
    dishes = [
        {
            'dish_uri': dish['dish_uri'],
            'votes_count': dish['votes_count'],
            'voted_by_user': dish['dish_uri'] in voted_list
        } for dish in dish_list
    ]
    print(dishes)
    return dishes

display_vote_options(1, "user1@gmail.com")


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
    return groups

def display_group_members(group_id):
    response, _ = supabase_client.table("Group Members Info")\
                        .select("email, status, User Registration (firstname, lastname)")\
                        .eq("group_id", group_id)\
                        .gt("status", 0)\
                        .execute()
    response_list = response[1]
    members = [
        {
            'email': member['email'],
            'first_name': member['User Registration']['firstname'],
            'last_name': member['User Registration']['lastname'],
            'stauts': member['status']
        } for member in response_list
    ]
    return members

# display the top dish url that has the most votes (LIMIT 5)
def display_top_votes(group_id):
    voted_food, _ = supabase_client.table("Group Food List")\
                    .select("dish_uri")\
                    .eq("group_id", group_id)\
                    .gt("votes_count", 0)\
                    .order("votes_count", desc=True)\
                    .limit(5)\
                    .execute()
    voted_food_list = voted_food[1]
    return voted_food_list

# When the user click the food, check if he's alr voted for 3, if yes, error, if not add that to the vote count
def click_vote_dish(group_id, user_email, dish_uri):
    valid_click = False
    
    # Give the count of how many times this user has voted
    num_voted, _ = supabase_client.table("Group Vote")\
                    .select('*')\
                    .eq("group_id", group_id)\
                    .eq("email", user_email)\
                    .execute()
    count = len(num_voted[1])
    
    # Get the status of this user
    status, _ = supabase_client.table("Group Members Info")\
                        .select("status")\
                        .eq("email", user_email)\
                        .eq("group_id", group_id)\
                        .execute()
    status_list = status[1]
    if len(status_list) == 0:
        user_status = 0
    else:
        user_status = status_list[0]['status']
    
    # Validate if the user has the right to vote
    if user_status == 2:
        if count < 11:
            valid_click = True
    if user_status == 1:
        if count < 4:
            valid_click = True
    
    # If valid to vote, add the dish uri to the table
    if valid_click:
        data_to_insert = {
            'group_id': group_id,
            'dish_uri': dish_uri,
            'email': user_email
        }
        # Insert the data into Group Vote
        data, _ = supabase_client.table("Group Vote")\
                    .insert([data_to_insert])\
                    .execute()
        
        # Get the updated count
        new_count, _ = supabase_client.table("Group Vote")\
                    .select('*')\
                    .eq("group_id", group_id)\
                    .eq("dish_uri", dish_uri)\
                    .execute()
        new_count = len(new_count[1])
        
        # Update the vote count in the Group Food List table
        data, _ = supabase_client.table("Group Food List")\
                    .update({"votes_count": new_count})\
                    .eq("dish_uri", dish_uri)\
                    .eq("group_id", group_id)\
                    .execute()
        print("Sucessfully voted")
    else:
        print("Vote is not sucessful. Check your condition")

########################################
##########    Sample Usage    ##########
########################################
