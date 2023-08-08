#!/usr/bin/env python3
import boto3
import datetime

ec2 = boto3.client('ec2')
now = datetime.datetime.now()

# Retrieve a list of EC2 instances
response = ec2.describe_instances()

# Extract and print instance information and tags
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_info = {
            'InstanceID': instance['InstanceId'],
            'InstanceType': instance['InstanceType'],
            'State': instance['State']['Name']
        }

        # Retrieve and print instance tags
        tags = instance.get('Tags', [])
        if tags:
            instance_info['Tags'] = tags

        print("Instance ID:", instance_info['InstanceID'])
        print("Instance Type:", instance_info['InstanceType'])
        print("State:", instance_info['State'])

        if 'Tags' in instance_info:
            print("Tags:")
            for tag in instance_info['Tags']:
                print(f"- {tag['Key']}: {tag['Value']}")
        
        print("-" * 30)
