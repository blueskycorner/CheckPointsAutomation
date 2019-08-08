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

# TODO
def getAllowedPorts(engine):
    portMin = 0
    portMax = 0
    if engine == "mysql":
        portMin = 3306
        portMax = 3306
    else:
        raise Exception("RDS engine not known for port checking")
    return portMin, portMax

def evaluate_compliance(configuration_item):
    try:
        compliance_status = "NON_COMPLIANT"

        if "engine" in configuration_item["configuration"] and \
                    configuration_item["configuration"]["engine"] != None and \
                    "endpoint" in configuration_item["configuration"] and \
                    configuration_item["configuration"]["endpoint"] != None :
            engine = configuration_item["configuration"]["engine"]
            
            portMin, portMax = getAllowedPorts(engine)
            endpoint = configuration_item["configuration"]["endpoint"]
            if "port" in endpoint and endpoint["port"] != None:
                port = endpoint["port"]
                if port >= portMin and port <= portMax:
                    compliance_status = "COMPLIANT"
            else:
                raise Exception("Missing port information")
        else:
            raise Exception("Missing engine or endpoint information")

    except Exception as e:
        print("evaluate_compliance: Error while evaluating the rule")
        print(traceback.format_exc())
        raise e

    return compliance_status


def lambda_handler(event, context):
    try:
        configuration_item, result_token, ruleParameters = init(event)

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
        print("RDSPortRule_lambda_handler: Error while evaluating the rule")
        print(traceback.format_exc())
        print(str(e))
        error = {"message": str(e)}
        sendError(sns, error, errorTopicArn)

    return evaluation['ComplianceType']