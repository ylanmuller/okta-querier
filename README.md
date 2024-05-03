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
- A read-only token to your Okta environment

## Getting Started
Clone the repository and adjust the following variables:

- Add your read-only token into the `headers` variable
- Adjust the `oktaDomain` variable to use your custom domain.

Set it to be an executable with `chmod + x /path/to/utility`.

You should be ready to use the utility!