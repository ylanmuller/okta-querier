#!/bin/env/usr python
# This utility lets you quickly pull up details about your Okta organization

import requests

# Replace <Okta API Token> with a token from your environment
headers = {"Authorization": "SSWS <Okta API Token>"}
# Enter your custom domain with .okta.com at the end
oktaDomain = ".okta.com"

def mainMenuChoice():
    continueDecision = input("Would you like to return to the main menu? y/n: ")
    if continueDecision == "y":
        mainMenu()
    elif continueDecision == "n":
        exit
    else:
        print("That is not a valid selection. Please try again.")
        mainMenuChoice()

def getUserDetails():
    # Lets you enter the email address of a user you want to look up, fetches the first match, and prints info
    username = input("Enter the exact email address of an active user you want to look up: ")
    findUserEndpoint = "https://" + oktaDomain + "/api/v1/users?search=profile.email Eq \"" + username + "\""
    findUserDetails = requests.get(findUserEndpoint, headers=headers).json()
    if findUserDetails:
        userInfo = findUserDetails[0]
        getUserGroupsEndpoint = "https://" + oktaDomain + f"/api/v1/users/{userInfo["id"]}/groups"
        getUserGroups = requests.get(getUserGroupsEndpoint, headers=headers).json()
        getUserAppsEndpoint = "https://" + oktaDomain + f"/api/v1/users/{userInfo["id"]}/appLinks"
        getUserApps = requests.get(getUserAppsEndpoint, headers=headers).json()

        # Modify this blob with the any fields from the profile that you want to include!
        print(f"-----PROFILE DETAILS FOR {username}-----\n\nName: {userInfo["profile"]["firstName"]} {userInfo["profile"]["lastName"]}\nUser Status: {userInfo["status"]}\nDepartment: {userInfo["profile"]["department"]}\nManager Email: {userInfo["profile"]["managerEmail"]}\n\n")

        # Prints all of the user's groups
        userGroups = ""
        for group in getUserGroups:
            userGroups = userGroups + group["profile"]["name"] + "\n"

        print(f"-----LIST OF USER'S GROUPS-----\n\n{userGroups}")

        # Prints all of the user's assigned applications
        userApps = ""
        for app in getUserApps:
            userApps = userApps + app["label"] + "\n"
        
        print(f"-----LIST OF USER'S APPS-----\n\n{userApps}")
        mainMenuChoice()

    else:
        print("That user either does not exist in Okta or is inactive.")
        mainMenuChoice()

def getAppDetails():
    # Lets you enter an app name, pull up a list of the applicable apps, enter the ID of the one you want to dig into, and then pull up details about it.
    appName = input("Enter the name of the app you want to find: ")
    findAppEndpoint = "https://" + oktaDomain + f"/api/v1/apps?q={appName}"
    findApps = requests.get(findAppEndpoint, headers=headers).json()

    if findApps:
        appInfo = ""
        for app in findApps:
            appInfo = appInfo + f"Name: {app["label"]} | Id: {app["id"]}\n"
        print(appInfo)
        appId = input("Copy, paste, and submit the ID of the app you want more information on: ")
        getAppDetailsEndpoint = "https://" + oktaDomain + f"/api/v1/apps/{appId}"
        getAppDetails = requests.get(getAppDetailsEndpoint, headers=headers).json()
        getAssociatedGroupsEndpoint = "https://" + oktaDomain + f"/api/v1/apps/{appId}/groups"
        getAssociatedGroups = requests.get(getAssociatedGroupsEndpoint, headers=headers).json()

        # Print some basic details about the application
        print(f"-----APP DETAILS FOR {getAppDetails["label"]}-----\n\nName: {getAppDetails["name"]}\nStatus: {getAppDetails["status"]}\nSign-on Mode: {getAppDetails["signOnMode"]}\n\n")

        # Tidies up groups
        # Will also add the ability to query the ID of the group and pull the name into the line
        groupList = ""
        for group in getAssociatedGroups:
            getGroupDetailsEndpoint = "https://" + oktaDomain + f"/api/v1/groups/{group["id"]}"
            getGroupDetails = requests.get(getGroupDetailsEndpoint, headers=headers).json()
            groupList = groupList + f"{getGroupDetails["profile"]["name"]} | {group["id"]} | Priority: {group["priority"]}\n"

        print("-----ASSIGNED GROUPS-----\n\n" + groupList)
    else:
        print("We were not able to find that app.")
        mainMenuChoice()

def getGroupDetails():
    # Lets you enter the name of a group and returns a list of all potential matches
    groupName = input("Enter the name of the group you want to find. HINT: Start from the beginning of the name: ")
    findGroupEndpoint = "https://" + oktaDomain + f"/api/v1/groups?q={groupName}"
    findGroups = requests.get(findGroupEndpoint, headers=headers).json()

    if findGroups:
        groupInfo = ""
        for group in findGroups:
            groupInfo = groupInfo + f"Name: {group["profile"]["name"]} | Id: {group["id"]}\n"
        print(groupInfo)
        groupId = input("Copy, paste, and submit the ID of the group you want more information on: ")
        getGroupDetailsEndpoint = "https://" + oktaDomain + f"/api/v1/groups/{groupId}"
        getGroupDetails = requests.get(getGroupDetailsEndpoint, headers=headers).json()

        # Print details about the group
        print(f"-----GROUP DETAILS FOR {getGroupDetails["profile"]["name"]}-----\n\nId: {getGroupDetails["id"]}\nDescription: {getGroupDetails["profile"]["description"]}\nCreated: {getGroupDetails["created"]}\nLast Membership Updated: {getGroupDetails["lastMembershipUpdated"]}\n\n")

        # Print all users
        getAssociatedUsersEndpoint = "https://" + oktaDomain + f"/api/v1/groups/{groupId}/users"
        getAssociatedUsers = requests.get(getAssociatedUsersEndpoint, headers=headers).json()

        if getAssociatedUsers:
            associatedUsers = ""
            for user in getAssociatedUsers:
                associatedUsers = associatedUsers + f"{user["profile"]["firstName"]} {user["profile"]["lastName"]} | Status: {user["status"]}\n"
            print("-----MEMBERS-----\n\n" + associatedUsers)
        else:
            print("There are no users in this group.")
            mainMenuChoice()
    else:
        print("We were not able to find a matching group.")
        mainMenuChoice()

def mainMenu():
    print("What would you like to do today? Enter the number that corresponds to what you want to do from the list.\n1: Get user details\n2: Get app details\n3: Get group details")
    choice = input("Make your selection: ")
    if choice == "1":
        getUserDetails()
    elif choice == "2":
        getAppDetails()
    elif choice =="3":
        getGroupDetails()
    else:
        print("Sorry, that choice is not valid! Try again.")
        mainMenu()

mainMenu()