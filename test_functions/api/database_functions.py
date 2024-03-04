from dotenv import load_dotenv 
import supabase
import os

load_dotenv()

# Constants for Supabase URL and API keys
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize the Supabase Client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def create_group(group_name, email_list, description):
    # Create group and retrieve group_id
    group_data = add_group_to_groupbase(group_name, description)
    group_id = group_data[0]['group_id']
    print(group_id)

    # Assuming the first person in the email list is the group owner (status 2)
    add_member_to_group(group_id, email_list[0], 2)
    # Add other members to Group Members Info, and set their status to pending (status 0) by default
    for email in email_list[1:]:
        add_member_to_group(group_id, email, 0)
    return

def add_group_to_groupbase(group_name, description):
    data_to_insert = {
        "group_name": group_name,
        "description": description
    }
    data, _ = supabase_client.table("Group Registration").insert([data_to_insert]).execute()
    # print(data)
    return data[1]

def add_member_to_group(group_id, email, status):
    data_to_insert = {
        "group_id": group_id,
        "email": email,
        "status": status
    }
    supabase_client.table("Group Members Info").insert([data_to_insert]).execute()
    return

# Display the groups that this user is part of / is invited
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

# Display the group members in the specified groups
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

# When the user click the food, check if he's alr voted for 3, if yes, error,
# if not add that to the vote count
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