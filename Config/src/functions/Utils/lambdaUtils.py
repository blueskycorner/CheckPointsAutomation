import json
import logging
import traceback

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def init(event):
    try:
        logger.info("Event: " + json.dumps(event))
        invoking_event = json.loads(event["invokingEvent"])
        configuration_item = invoking_event["configurationItem"]
        result_token = "No token found."
        if "resultToken" in event:
            result_token = event["resultToken"]
    except Exception as e:
        print("init: Error while processing inputs")
        print(traceback.format_exc())
        raise e

    return configuration_item, result_token

def buildEvaluation(configuration_item, compliance_status, annotation):
    try:
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
    except Exception as e:
        print("init: Error while building evaluation")
        print(traceback.format_exc())
        raise e

    return evaluation


def sendError(sns, errorMessage, errorTopicArn):

    try:
        print(errorMessage)
        
        response = sns.publish(
            TargetArn=errorTopicArn,
            Message=json.dumps({'default': json.dumps(errorMessage)}),
            MessageStructure='json')

        print("topicPush: " + response)
    except Exception as e:
        print("init: Error while processing inputs")
        raise e