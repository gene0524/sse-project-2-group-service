from flask import Flask, jsonify, request
from flask_cors import CORS 
from database_functions import create_group, display_groups, display_group_members, display_top_votes, click_vote_dish

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

@app.route('/display-groups', methods=['POST'])
def display_user_groups():
    try:
        request_data = request.json
        user_email = request_data.get('userEmail')
        groups = display_groups(user_email)
        
        # groups in the form 
        #groups =
        #{
        #    'group_name': ,
        #    'description': ,
        #    'group_id': ,
        #    'status': 
        #}
        
        return jsonify(groups=groups)
    except Exception as e:
        return jsonify(error=str(e)), 500    
    
@app.route('/display-group-members', methods=['POST'])
def display_group_members_route():
    try:
        request_data = request.json
        group_id = request_data.get('groupId')
        members = display_group_members(group_id)
        
        """ format of members
        members =
        {
            'email': member['email'],
            'first_name': member['User Registration']['firstname'],
            'last_name': member['User Registration']['lastname'],
            'stauts': member['status']
        } 
        """
        return jsonify(members=members)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/display-top-votes', methods=['POST'])
def display_group_top_votes():
    try:
        request_data = request.json
        group_id = request_data.get('groupId')
        top_votes = display_top_votes(group_id)
        return jsonify(topDishes=top_votes)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/click-vote-dish', methods=['POST'])
def click_vote_dish_route():
    try:
        request_data = request.json
        group_id = request_data.get('groupId')
        user_email = request_data.get('userEmail')
        dish_uri = request_data.get('dishUri')
        click_vote_dish(group_id, user_email, dish_uri)
        return jsonify(message='Vote registered successfully')
    except Exception as e:
        return jsonify(error=str(e)), 500
