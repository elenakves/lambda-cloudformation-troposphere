"""
cfn template for DynamoDB table
"""
from troposphere import Output, Parameter, Ref, Template
from troposphere.dynamodb import (KeySchema, AttributeDefinition,
                                   ProvisionedThroughput)
from troposphere.dynamodb import Table

t = Template()

t.set_description("Create DynamoDB table for app")

hashkeyname = t.add_parameter(Parameter(
    "HaskKeyElementName",
    Description="HashType PrimaryKey Name",
    Type="String",
	Default="userId",
    AllowedPattern="[a-zA-Z0-9]*",
    MinLength="1",
    MaxLength="2048",
    ConstraintDescription="must contain only alphanumberic characters"
))

hashkeytype = t.add_parameter(Parameter(
    "HaskKeyElementType",
    Description="HashType PrimaryKey Type",
    Type="String",
    Default="S",
    AllowedPattern="[S|N]",
    MinLength="1",
    MaxLength="1",
    ConstraintDescription="must be either S or N"
))


readunits = t.add_parameter(Parameter(
    "ReadCapacityUnits",
    Description="Provisioned read throughput",
    Type="Number",
    Default="1",
    MinValue="1",
    MaxValue="1",
    ConstraintDescription="should be between 1 and 5"
))

writeunits = t.add_parameter(Parameter(
    "WriteCapacityUnits",
    Description="Provisioned write throughput",
    Type="Number",
    Default="1",
    MinValue="1",
    MaxValue="1",
    ConstraintDescription="should be between 1 and 5"
))

t.add_resource(Table(
    "LambdaAppDynamoDB",
    AttributeDefinitions=[
        AttributeDefinition(
            AttributeName=Ref(hashkeyname),
            AttributeType=Ref(hashkeytype)
        )
    ],
    KeySchema=[
        KeySchema(
            AttributeName=Ref(hashkeyname),
            KeyType="HASH"
        )
    ],
    ProvisionedThroughput=ProvisionedThroughput(
        ReadCapacityUnits=Ref(readunits),
        WriteCapacityUnits=Ref(writeunits)
    )
))

