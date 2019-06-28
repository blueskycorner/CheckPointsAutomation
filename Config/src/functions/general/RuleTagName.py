import json
import os
import boto3
import logging
import traceback

from src.functions.Utils.lambdaUtils import init, buildEvaluation, sendError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = boto3.client("config")
sns = boto3.client('sns')

annotation = "Tag Name must be present and not empty"
errorTopicArnParamName = "configErrorTopicArn"
errorTopicArn = os.getenv(errorTopicArnParamName)

def evaluate_compliance(configuration_item):
    try:
        compliance_status = "NON_COMPLIANT"

        if "configuration" in configuration_item and configuration_item["configuration"] != None:
            for tag in configuration_item["configuration"]["tags"]:
                if tag["key"] == "Name":
                    if tag["value"]:
                        compliance_status = "COMPLIANT"
    except Exception as e:
        print("evaluate_compliance: Error while evaluating the rule")
        print(traceback.format_exc())
        raise e

    return compliance_status


def lambda_handler(event, context):
    try:
        configuration_item, result_token = init(event)

        compliance_status = "NOT_APPLICABLE"

        if "eventLeftScope" in event and event["eventLeftScope"] == False:
            compliance_status = evaluate_compliance(configuration_item)

        evaluation = buildEvaluation(configuration_item, compliance_status, annotation)

        if "dryRun" not in event:
            config.put_evaluations(
                Evaluations=[evaluation],
                ResultToken=result_token
                )
    except Exception as e:
        print("lambda_handler: Error while evaluating the rule")
        print(traceback.format_exc())
        print(str(e))
        error = {"message": str(e)}
        sendError(sns, error, errorTopicArn)

    return evaluation['ComplianceType']