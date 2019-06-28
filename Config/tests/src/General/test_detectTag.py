import json
from src.functions.general.DetectTagRule import evaluate_compliance 

# content of test_sample.py
def getInput(input):
    input = 'tests/inputs/Tag/' + input
    with open(input) as json_file:  
        event = json.load(json_file)
        print(event)
        return event

def evalution(input, tagLabel):
    event = getInput(input)
    configuration_item = event["configurationItem"]
    compliance_status = evaluate_compliance(configuration_item, tagLabel)
    return compliance_status

# Tag Name
def test_tagNameCompliant():
    compliance_status = evalution("SecurityGroupInvokeEventTagNameOK.json", "Name")
    assert compliance_status == "COMPLIANT"

def test_tagNameMissing():
    compliance_status = evalution("SecurityGroupInvokeEventTagNameMissing.json", "Name")
    assert compliance_status == "NON_COMPLIANT"

def test_tagNameCaseSensitive():
    compliance_status = evalution("SecurityGroupInvokeEventTagNameCaseSensitive.json", "Name")
    assert compliance_status == "NON_COMPLIANT"

def test_tagNameEmpty():
    compliance_status = evalution("SecurityGroupInvokeEventTagNameEmpty.json", "Name")
    assert compliance_status == "NON_COMPLIANT"

# Tag app-name
def test_tagAppNameOK():
    compliance_status = evalution("SecurityGroupInvokeEventTagAppNameOK.json", "app-name")
    assert compliance_status == "COMPLIANT"