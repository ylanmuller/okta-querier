# Okta Querier
Lightweight utility that lets you fetch basic information about Okta users, apps, and groups. It does not currently have any write functionality.

Currently supports the following: 

- Entering an email address for a user and fetching:
    - Basic profile details (can be adjusted to your own liking)
    - All group memberships
    - All assigned applications
- Entering a group name (currently only works if you search from the start of a string, not unlike Okta's search) and fetching:
    - Basic group details
    - Users assigned to the group and their status
- Entering an application name (which is based on the name Okta uses for it in their API, NOT the human readable name, although it will let you choose from a list of results) and fetching:
    - Basic app details
    - Which groups are assigned and in what order

## Prerequisites
- Python install
- The **requests**, **webbrowser**, and **time**, and Python modules (installable by running `python3 -m pip install module_name`)

## Getting Started
Clone the repository and adjust the following variables:

- Adjust the `base_url` variable to use your custom domain.
- Create an OIDC app in Okta and retrieve the Client Id value:
    1. From Okta go to Applications > Applications > Create App Integration and select "OIDC". Set app type to "Native."
    2. Check "Device Authorization" on the next page
    3. Assign a group of users who will be allowed to authorize the app to your environment. You can skip this and do it later from the Assignments tab.
    4. Go to "Okta API Scopes" and configure the following scopes:
        - okta.users.read
        - okta.groups.read
        - okta.apps.read
    5. Copy the Client ID from the "General" tab and update the `client_id` variable
- Set it to be an executable with `chmod +x /path/to/utility`.

You should be ready to use the utility!

## Customization

You can adjust the print statement under line 33 to include additional profile details, such as custom fields, by using this syntax:

`\nField Name: {userInfo["profile"]["fieldApiName"]}`

I recommend running a one-off API call to fetch a user in your Okta environment to easily see what your field API names are, but you can also find them in Okta's profile editor. This customization guidance applies to other print statements in the utility as well.