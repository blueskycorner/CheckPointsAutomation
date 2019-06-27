import json
from CheckPointsAutomation.Config.src.functions.general.TagName import evaluate_compliance 

# content of test_sample.py
def getInput(input):
    input = 'CheckPointsAutomation/Config/tests/inputs/Tag/' + input
    with open(input) as json_file:  
        event = json.load(json_file)
        print(event)
        return event

def evalution(input):
    event = getInput(input)
    configuration_item = event["configurationItem"]
    compliance_status = evaluate_compliance(configuration_item)
    return compliance_status


def test_tagNameCompliant():
    compliance_status = evalution("SecurityGroupInvokeEventTagNameOK.json")
    assert compliance_status == "COMPLIANT"

def test_tagNameMissing():
    compliance_status = evalution("SecurityGroupInvokeEventTagNameMissing.json")
    assert compliance_status == "NON_COMPLIANT"

def test_tagNameCaseSensitive():
    compliance_status = evalution("SecurityGroupInvokeEventTagNameCaseSensitive.json")
    assert compliance_status == "NON_COMPLIANT"

def test_tagNameEmpty():
    compliance_status = evalution("SecurityGroupInvokeEventTagNameEmpty.json")
    assert compliance_status == "NON_COMPLIANT"