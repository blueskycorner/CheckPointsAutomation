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
    compliance_status = None
    try:
        event = getInput(input)
        configuration_item = event["configurationItem"]
        compliance_status = evaluate_compliance(configuration_item)
    except Exception as e:
        print(str(e))
    return compliance_status

# MySQL 
def test_mysqlPortCompliant():
    compliance_status = evalution("RDSInstance_mysql_OK.json")
    assert compliance_status == "COMPLIANT"
    
def test_mysqlPortNotCompliant():
    compliance_status = evalution("RDSInstance_mysql_KO.json")
    assert compliance_status == "NON_COMPLIANT"
    
def test_noengine():
    compliance_status = evalution("RDSInstance_noengine.json")
    assert compliance_status == None
    
if __name__ == "__main__":
    test_noengine()