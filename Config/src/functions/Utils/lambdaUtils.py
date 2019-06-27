import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def init(event):
    logger.info("Event: " + json.dumps(event))
    invoking_event = json.loads(event["invokingEvent"])
    configuration_item = invoking_event["configurationItem"]
    result_token = "No token found."
    if "resultToken" in event:
        result_token = event["resultToken"]

    return configuration_item, result_token

def buildEvaluation(configuration_item, compliance_status, annotation):
    evaluation = {
        "ComplianceResourceType":
            configuration_item["resourceType"],
        "ComplianceResourceId":
            configuration_item["resourceId"],
        "ComplianceType":
            compliance_status,
        "Annotation":
            annotation,
        "OrderingTimestamp":
            configuration_item["configurationItemCaptureTime"]
    }

    return evaluation