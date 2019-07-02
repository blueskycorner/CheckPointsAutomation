#!/bin/bash

aws configservice describe-compliance-by-resource --compliance-types NON_COMPLIANT --profile hardis > describe-compliance-by-resource_NON_COMPLIANT.json
aws configservice get-compliance-details-by-resource --resource-type AWS::EC2::SecurityGroup --resource-id sg-002b80fdb55e8f0cc --compliance-types NON_COMPLIANT --profile hardis

aws configservice batch-get-resource-config --resource-keys resourceType=AWS::RDS::DBInstance,resourceId=db-ODKMWZQ66B46CGZDEOFDBEMZHQ

aws configservice get-resource-config-history --resource-type AWS::EC2::SecurityGroup --resource-id sg-002b80fdb55e8f0cc --profile hardis
aws configservice get-discovered-resource-counts --profile hardis

aws configservice deliver-config-snapshot --delivery-channel-name BaseConfig-dev-ConfigDeliveryChannel-1NXY5K8ZBNJ0D
aws resourcegroupstaggingapi get-resources --tag-filters Key=app-name,Values=app1 --profile hardis