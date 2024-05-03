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
    username = input("Enter the email address of an active user you want to look up: ")
    findUserEndpoint = "https://" + oktaDomain + "/api/v1/users?q=" + username
    findUserDetails = requests.get(findUserEndpoint, headers=headers).json()
    if findUserDetails:
        # Runs if the array received is not empty
        userInfo = findUserDetails[0]
        getUserGroupsEndpoint = "https://" + oktaDomain + f"/api/v1/users/{userInfo["id"]}/groups"
        getUserGroups = requests.get(getUserGroupsEndpoint, headers=headers).json()
        getUserAppsEndpoint = "https://" + oktaDomain + f"/api/v1/users/{userInfo["id"]}/appLinks"
        getUserApps = requests.get(getUserAppsEndpoint, headers=headers).json()

        # Modify this blob with the any fields from the profile that you want to include!
        print(f"-----PROFILE DETAILS FOR {username}-----\n\nName: {userInfo["profile"]["firstName"]} {userInfo["profile"]["lastName"]}\nUser Status: {userInfo["status"]}\nDepartment: {userInfo["profile"]["department"]}\nManager Email: {userInfo["profile"]["managerEmail"]}\nOnboarding Completed?: {userInfo["profile"]["onboardingComplete"]}\nBeyond Identity Registered?: {userInfo["profile"]["byndidRegistered"]}\n\n")

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
    print("We'll get you those details soon.")
    # This should be able to let you enter an app name, pull up a list of the applicable apps, let you enter the ID of the one you want to dig into, and then pull up details about it.
    appName = input("Enter the name of the app you want to find: ")
    findAppEndpoint = "https://" + oktaDomain + f"/api/v1/apps?q={appName}"
    findApps = requests.get(findAppEndpoint, headers=headers).json()

    if findApps:
    # Runs if array received is not empty
        appInfo = ""
        for app in findApps:
            appInfo = appInfo + f"Name: {app["label"]} | Id: {app["id"]}\n"
        print(appInfo)
        appId = input("Copy, paste, and submit the ID of the app you want more information on: ")
        getAppDetailsEndpoint = "https://" + oktaDomain + f"/api/v1/apps/{appId}"
        getAppDetails = requests.get(getAppDetailsEndpoint, headers=headers).json()
        getAssociatedGroupsEndpoint = "https://" + oktaDomain + f"/api/v1/apps/{appId}/groups"
        getAssociatedGroups = requests.get(getAssociatedGroupsEndpoint, headers=headers).json()

        # Print some basic details as well as which groups and users are assigned
        print(f"-----APP DETAILS FOR {getAppDetails["label"]}-----\n\nName: {getAppDetails["name"]}\nStatus: {getAppDetails["status"]}\nSign-on Mode: {getAppDetails["signOnMode"]}\n\n")

        # Clean up groups
        # Will also add the ability to query the ID of the group and pull the name into the line
        groupList = ""
        for group in getAssociatedGroups:
            groupList = groupList + f"{group["id"]} | Priority: {group["priority"]}\n"

        print(groupList)
    else:
        print("We were not able to find that app.")
        mainMenuChoice()

def mainMenu():
    print("What would you like to do today? Enter the number that corresponds to what you want to do from the list.\n1: Get user details\n2: Get app details")
    choice = input("Make your selection: ")
    if choice == "1":
        getUserDetails()
    elif choice == "2":
        getAppDetails()
    else:
        print("Sorry, that choice is not valid! Try again.")
        mainMenu()

mainMenu()