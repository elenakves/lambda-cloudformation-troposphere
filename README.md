# lambda-cloudformation-troposphere
********************************


Python code to deploy cloudformation template with troposphere.

The cfn stack includes Lambda, DynamoDB, CW schedule, IAM roles, S3 bucket to store deployment packages.

The infrastructure configuration templates/lambda_template.py is parametrized.

It allows to add any number of Lambda functions to the stack (add code to /lambda/ and include in create_and_deploy_cfn_template.py)

In this version, DynamoDB is not used at all, just added as an examlpe, to integrate in future.


## To start:

Start virtual env:
 
`virtualenv venv --python=python3`
 
`source venv/bin/activate`
 
Note: on Windows you might need to point to python.exe, e.g.: `virtualenv env -p C:/Python36/python.exe`

and: `env\Scripts\activate`


## Requirements

`pip install -r requirements.txt`


## Running it

Runtime Python3.6

Run create_and_deploy_cfn_template.py

This will output cfn template and create cfn stack.


## Tests

example event to test:
{
  "id": "cdc73f9d-aea9-11e3-9d5a-835b769c0d9c",
  "detail-type": "Scheduled Event",
  "source": "aws.events",
  "account": "{{account-id}}",
  "time": "1970-01-01T00:00:00Z",
  "region": "eu-west-1",
  "resources": [
    "arn:aws:events:eu-west-1:123456789012:rule/ExampleRule"
  ],
  "detail": {}
}


## ToDo


This is a work in progress
 - build tests

