#!/usr/bin/env python3
import boto3
import datetime

ec2 = boto3.client('ec2')
now = datetime.datetime.now()

# Specify the instance ID of the EC2 instance you want to start
instance_id = 'i-0c696286c9a30e840'

# Start the EC2 instance
response = ec2.start_instances(
    InstanceIds=[instance_id]
)

print("Instance starting:", now)