import json
import boto3
import logging

from CheckPointsAutomation.Config.src.functions.Utils.lambdaUtils import init, buildEvaluation

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = boto3.client("config")

annotation = "Tag Name must be present and not empty"

def evaluate_compliance(configuration_item):
    compliance_status = "NON_COMPLIANT"

    for tag in configuration_item["configuration"]["tags"]:
        if tag["key"] == "Name":
            if tag["value"]:
                compliance_status = "COMPLIANT"

    return compliance_status


def lambda_handler(event, context):
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

    return evaluation['ComplianceType']