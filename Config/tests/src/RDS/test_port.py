import json
# import sys
# print(sys.path)
from src.functions.RDS.RDSPortRule import evaluate_compliance 

# content of test_sample.py
def getInput(input):
    input = 'tests/inputs/RDS/' + input
    with open(input) as json_file:  
        event = json.load(json_file)
        print(event)
        return event

def evalution(input):
    event = getInput(input)
    configuration_item = event["configurationItem"]
    compliance_status = evaluate_compliance(configuration_item)
    return compliance_status

# Tag Name
def test_mysqlPortCompliant():
    compliance_status = evalution("RDSInstance_mysql_OK.json")
    assert compliance_status == "COMPLIANT"
    
if __name__ == "__main__":
    test_mysqlPortCompliant()