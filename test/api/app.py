from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS 
import supabase
import os

load_dotenv()

# Constants for Supabase URL and API keys
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize the Supabase Client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
CORS(app) 

@app.route('/submit-group', methods=['POST'])
def submit_group():
    try:
        print('Received raw data:', request.data)

        # Get the JSON data from the request
        group_data = request.json

        # Do something with the received data
        print('Received group data:', group_data)

        # Trigger create_group function to store data in the database
        create_group(
            group_name=group_data.get('groupName'),
            email_list=group_data.get('groupMembers'),
            description=group_data.get('groupDetail')
        )

        # Return a success message
        return jsonify(message='Group data received successfully')
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/", methods=["GET"])
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
