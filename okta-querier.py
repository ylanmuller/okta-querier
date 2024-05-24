#!/bin/env/usr python
# This utility lets you quickly pull up details about your Okta organization from a CLI interface

import requests
import webbrowser
import time

# Authorize against the OIDC app configured in your Okta tenant. Code courtesy of gabrielsokra: https://github.com/gabrielsroka
# Set these values. See the README for more information:
base_url = 'https://your_domain.okta.com'
client_id = 'OIDC APP Client Id'
scope = 'okta.users.read okta.groups.read okta.apps.read'

auth_url = base_url + '/oauth2/v1/device/authorize'
auth_payload = {
    'client_id': client_id,
    'scope': 'openid ' + scope
}
auth = requests.post(auth_url, data=auth_payload).json()
webbrowser.open_new(auth['verification_uri_complete'])

while True:
    time.sleep(2)
    token_url = base_url + '/oauth2/v1/token'
    token_payload = {
        'client_id': client_id,
        'device_code': auth['device_code'],
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
    }
    tokens = requests.post(token_url, data=token_payload).json()
    access_token = tokens.get('access_token')
    if access_token: break

session = requests.Session()
session.headers['authorization'] = 'Bearer ' + access_token

# Handling for whether to be returned to the main manu
def main_menu_choice():
    continue_decision = input('Would you like to return to the main menu? y/n: ')
    if continue_decision == 'y':
        main_menu()
    elif continue_decision == 'n':
        exit
    else:
        print('That is not a valid selection. Please try again.')
        main_menu_choice()

# Lets you enter the email address of a user you want to look up, fetches the first match, and prints info
def get_user_details():
    email = input('Enter the exact email address of an active user you want to look up: ')
    find_user_endpoint = base_url + '/api/v1/users?search=profile.email Eq ' + '"' + email + '"'
    find_user_details = session.get(find_user_endpoint).json()
    if find_user_details:
        user_info = find_user_details[0]
        get_user_groups_endpoint = base_url + f'/api/v1/users/{user_info['id']}/groups'
        get_user_groups = session.get(get_user_groups_endpoint).json()
        get_user_apps_endpoint = base_url + f'/api/v1/users/{user_info['id']}/appLinks'
        get_user_apps = session.get(get_user_apps_endpoint).json()

        # Modify this blob with the any fields from the profile that you want to include!
        print(f'-----PROFILE DETAILS FOR {email}-----\n\nName: {user_info['profile']['firstName']} {user_info['profile']['lastName']}\nUser Status: {user_info['status']}\nDepartment: {user_info['profile']['department']}\nManager Email: {user_info['profile']['managerEmail']}\n\n')

        # Prints all of the user's groups
        user_groups = ''
        for group in get_user_groups:
            user_groups = user_groups + group['profile']['name'] + '\n'

        print(f'-----LIST OF USER\'S GROUPS-----\n\n{user_groups}')

        # Prints all of the user's assigned applications
        user_apps = ''
        for app in get_user_apps:
            user_apps = user_apps + app['label'] + '\n'
        
        print(f'-----LIST OF USER\'S APPS-----\n\n{user_apps}')
        main_menu_choice()

    else:
        print('That user either does not exist in Okta or is inactive.')
        main_menu_choice()

# Lets you enter an app name, pull up a list of the applicable apps, enter the ID of the one you want to dig into, and then pull up details about it.
def get_app_details():
    app_name = input('Enter the name of the app you want to find: ')
    find_app_endpoint = base_url + f'/api/v1/apps?q={app_name}'
    find_apps = session.get(find_app_endpoint).json()

    if find_apps:
        app_info = ''
        for app in find_apps:
            app_info = app_info + f'Name: {app['label']} | Id: {app['id']}\n'
        print(app_info)
        app_id = input('Copy, paste, and submit the ID of the app you want more information on: ')
        get_app_details_endpoint = base_url + f'/api/v1/apps/{app_id}'
        get_app_details = session.get(get_app_details_endpoint).json()
        get_associated_groups_endpoint = base_url + f'/api/v1/apps/{app_id}/groups'
        get_associated_groups = session.get(get_associated_groups_endpoint).json()

        # Print some basic details about the application
        print(f'-----APP DETAILS FOR {get_app_details['label']}-----\n\nName: {get_app_details['name']}\nStatus: {get_app_details['status']}\nSign-on Mode: {get_app_details['signOnMode']}\n\n')

        # Tidies up groups
        # Will also add the ability to query the ID of the group and pull the name into the line
        group_list = ''
        for group in get_associated_groups:
            get_group_details_endpoint = base_url + f'/api/v1/groups/{group['id']}'
            get_group_details = session.get(get_group_details_endpoint).json()
            group_list = group_list + f'{get_group_details['profile']['name']} | {group['id']} | Priority: {group['priority']}\n'

        print('-----ASSIGNED GROUPS-----\n\n' + group_list)
        main_menu_choice()
    else:
        print('We were not able to find that app.')
        main_menu_choice()

# Lets you enter the name of a group and returns a list of all potential matches
def get_group_details():
    group_name = input('Enter the name of the group you want to find. HINT: Start from the beginning of the name: ')
    find_group_endpoint = base_url + f'/api/v1/groups?q={group_name}'
    find_groups = session.get(find_group_endpoint).json()

    if find_groups:
        group_info = ''
        for group in find_groups:
            group_info = group_info + f'Name: {group['profile']['name']} | Id: {group['id']}\n'
        print(group_info)
        group_id = input('Copy, paste, and submit the ID of the group you want more information on: ')
        get_group_details_endpoint = base_url + f'/api/v1/groups/{group_id}'
        get_group_details = session.get(get_group_details_endpoint).json()

        # Print details about the group
        print(f'-----GROUP DETAILS FOR {get_group_details['profile']['name']}-----\n\nId: {get_group_details['id']}\nDescription: {get_group_details['profile']['description']}\nCreated: {get_group_details['created']}\nLast Membership Updated: {get_group_details['lastMembershipUpdated']}\n\n')

        # Print all users
        get_associated_users_endpoint = base_url + f'/api/v1/groups/{group_id}/users'
        get_associated_users = session.get(get_associated_users_endpoint).json()

        if get_associated_users:
            associated_users = ''
            for user in get_associated_users:
                associated_users = associated_users + f'{user['profile']['firstName']} {user['profile']['lastName']} | Status: {user['status']}\n'
            print('-----MEMBERS-----\n\n' + associated_users)
            main_menu_choice()
        else:
            print('There are no users in this group.')
            main_menu_choice()
    else:
        print('We were not able to find a matching group.')
        main_menu_choice()

def main_menu():
    print('What would you like to do today? Enter the number that corresponds to what you want to do from the list.\n1: Get user details\n2: Get app details\n3: Get group details')
    choice = input('Make your selection: ')
    if choice == '1':
        get_user_details()
    elif choice == '2':
        get_app_details()
    elif choice =='3':
        get_group_details()
    else:
        print('Sorry, that choice is not valid! Try again.')
        main_menu()

main_menu()