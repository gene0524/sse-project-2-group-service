from flask import Flask, jsonify, request
from flask_cors import CORS 
from database_functions import create_group, display_user_groups, display_group_members,\
    display_top_votes, click_vote_dish, display_vote_options
import logging

app = Flask(__name__)
CORS(app) 

@app.route('/create-group', methods=['POST'])
def app_create_group():
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

@app.route('/display-user-groups', methods=['POST'])
def app_display_user_groups():
    try:
        request_data = request.json
        user_email = request_data.get('userEmail')
        logging.debug(f'Received request for user email: {user_email}')
        groups = display_user_groups(user_email)
        # groups = [
        #     {'group_name': group_name, 'description': description, 'group_id': group_id, 'status': status},
        #     {'group_name': group_name, 'description': description, 'group_id': group_id, 'status': status},
        #     {'group_name': group_name, 'description': description, 'group_id': group_id, 'status': status}
        # ]
        print(groups)
        return jsonify(groups=groups)
    except Exception as e:
        return jsonify(error=str(e)), 500    
    
@app.route('/display-group-members', methods=['POST'])
def app_display_group_members():
    try:
        request_data = request.json
        group_id = request_data.get('groupId')
        members = display_group_members(group_id)
        # members = [
        #     {'email': email, 'first_name': first_name,'last_name': last_name,'stauts': stauts},
        #     {'email': email, 'first_name': first_name,'last_name': last_name,'stauts': stauts},
        #     {'email': email, 'first_name': first_name,'last_name': last_name,'stauts': stauts}
        # ]
        return jsonify(members=members)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/display-top-votes', methods=['POST'])
def app_display_top_votes():
    try:
        request_data = request.json
        group_id = request_data.get('groupId')
        top_votes = display_top_votes(group_id)
        [{'dish_uri': 'Egg'}, {'dish_uri': 'Fish'}, {'dish_uri': 'Beef'}]
        # top_votes = [
        #     {'dish_uri': dish_uri},
        #     {'dish_uri': dish_uri},
        #     {'dish_uri': dish_uri}
        # ]
        return jsonify(topDishes=top_votes)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/click-vote-dish', methods=['POST'])
def app_click_vote_dish():
    try:
        request_data = request.json
        group_id = request_data.get('groupId')
        user_email = request_data.get('userEmail')
        dish_uri = request_data.get('dishUri')
        click_vote_dish(group_id, user_email, dish_uri)
        return jsonify(message='Vote registered successfully')
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/display-vote-options', methods=['POST'])
def app_display_vote_options():
    try:
        request_data = request.json
        group_id = request_data.get('groupId')
        user_email = request_data.get('userEmail')
        
        dish_uri = request_data.get('dishUri')
        votes = display_vote_options(group_id, user_email)
        #dishes = [
        #    {'dish_uri': dish_uri, 'votes_count': votes_count, 'voted_by_user': dish['dish_uri'] in voted_list
        #}
        #]
        return jsonify(allVotes=votes)
    except Exception as e:
        return jsonify(error=str(e)), 500
