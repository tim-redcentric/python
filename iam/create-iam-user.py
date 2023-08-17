#!/usr/bin/env python3

# Tim Samanchi - RedcentricPLC
# 17/08/2023

import boto3
import random
import string
import datetime
import time
import sys

# Change the values for the variables below to match your requirements
new_username = 'test.user@somedomain.com'
group_name = 'twc-readonly'

# Progress indicator as spinning cursor 
def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

spinner = spinning_cursor()

iam_client = boto3.client('iam')
session = boto3.session.Session()
now = datetime.datetime.now()

# Create a new IAM user: new_username
try:
    response = iam_client.create_user(UserName=new_username)
    print(f"User '{new_username}' created successfully")
except Exception as e:
    print(f"Error creating user: {e}")

# Add the user to a specific group: group_name
try:
    iam_client.add_user_to_group(UserName=new_username, GroupName=group_name)
    print(f"User '{new_username}' added to group '{group_name}' successfully")
except Exception as e:
    print(f"Error adding user to group: {e}")

# Generate a random password
password_length = 18

# Include symbols in the character pool for the generic password
characters = string.ascii_letters + string.digits + string.punctuation

# Generate the password without a symbol initially
password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(password_length - 1))

# Add a randomly generated symbol to the password
symbol = random.choice(string.punctuation)
position = random.randint(0, password_length - 1)
password = password[:position] + symbol + password[position:]

# Create login profile for console access
try:
    iam_client.create_login_profile(UserName=new_username, Password=password, PasswordResetRequired=False)
    print("Login profile created successfully")
except Exception as e:
    print(f"Error creating login profile: {e}")

# Wait for a short while to allow login profile creation to complete
print("Processing... ", end='', flush=True)

for _ in range(12):
    sys.stdout.write(next(spinner))
    sys.stdout.flush()
    time.sleep(1)
    sys.stdout.write('\b')
    sys.stdout.flush()

print("Completed!")

# Update the user's password status: uncheck user required to change password on 1st login
try:
    iam_client.update_login_profile(UserName=new_username, PasswordResetRequired=False)
    print("User password reset requirement disabled")
except Exception as e:
    print(f"Error updating login profile: {e}")

# Get the current region from the session and construct the console sign-in URL
current_region = session.region_name
print(f"Current AWS region {current_region}")

# Retrieve the account alias
try:
    response = iam_client.list_account_aliases()
    account_alias = response['AccountAliases'][0]
    print(f"Account Alias: {account_alias}")
except Exception as e:
    print(f"Error retrieving account alias: {e}")

console_signin_url = f'https://{account_alias}.signin.aws.amazon.com/console'
print(f"Console Sign-In URL for '{new_username}': {console_signin_url}")

# Print the generated password
print(f"Generated password for '{new_username}': {password}")
