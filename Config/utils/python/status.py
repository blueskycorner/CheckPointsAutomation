import json
import os
import boto3
import logging
import traceback

session = boto3.session.Session(profile_name='hardis')
config = session.client("config")

def main():
    print("start")
    NextToken = None
    response = config.describe_compliance_by_resource(
    # ResourceType='AWS::EC2::Instance',
    # ResourceId='string',
    ComplianceTypes=[
        "NON_COMPLIANT","COMPLIANT"
    ],
    Limit=100,
    # NextToken=''
    )
    print(response)

    if "NextToken" in response:
        NextToken = response["NextToken"]

    while NextToken:
        response = config.describe_compliance_by_resource(
        ComplianceTypes=[
            "NON_COMPLIANT","COMPLIANT"
        ],
        Limit=100,
        NextToken=NextToken
        )
        NextToken = None
        if "NextToken" in response:
            NextToken = response["NextToken"]
        print(response)


if __name__== "__main__":
    main()