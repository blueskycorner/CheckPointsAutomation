import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = boto3.client("config")


def evaluate_compliance(configuration_item):
    compliance_status = "NON_COMPLIANT"

    for tag in configuration_item["configuration"]["tags"]:
        if tag["key"] == "Name":
            if tag["value"]:
                compliance_status = "COMPLIANT"

    return compliance_status


def lambda_handler(event, context):
    logger.info("Event: " + json.dumps(event))
    invoking_event = json.loads(event["invokingEvent"])
    configuration_item = invoking_event["configurationItem"]
    result_token = "No token found."
    if "resultToken" in event:
        result_token = event["resultToken"]

    compliance_status = "NOT_APPLICABLE"

    if "eventLeftScope" in event and event["eventLeftScope"] == False:
        compliance_status = evaluate_compliance(configuration_item)

    
    evaluation = {
        "ComplianceResourceType":
            configuration_item["resourceType"],
        "ComplianceResourceId":
            configuration_item["resourceId"],
        "ComplianceType":
            compliance_status,
        "Annotation":
            "SSH Access is allowed to not allowed IP addess range",
        "OrderingTimestamp":
            configuration_item["configurationItemCaptureTime"]
    }

    if "dryRun" not in event:
        config.put_evaluations(
            Evaluations=[evaluation],
            ResultToken=result_token
            )

    return evaluation['ComplianceType']