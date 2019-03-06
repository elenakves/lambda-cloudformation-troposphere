"""
IAM Role Creation
This script creates the IAM Policies that Lambda functions need for execution
"""
from troposphere.iam import Policy

lambda_assume_role = {
    "Version": '2012-10-17',
    "Statement": [
        {"Effect": "Allow",
         "Principal": {"Service": ["lambda.amazonaws.com"]},
         "Action": ["sts:AssumeRole"]}]}

allow_lambda_execute = Policy(
    'AllowLambdaExecute',
    PolicyName='allow-lambda-execute',
    PolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": ["logs:CreateLogGroup",
                       "logs:CreateLogStream",
                       "logs:PutLogEvents"],
            "Resource": "*"}]})


allow_dynamodb_action = Policy(
    'AllowDynamodbAction',
    PolicyName='allow-dyanmoDB-action',
    PolicyDocument={
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": [
              "dynamodb:PutItem",
              "dynamodb:UpdateItem",
              "dynamodb:DeleteItem",
              "dynamodb:BatchGetItem",
              "dynamodb:DescribeTable",
              "dynamodb:GetItem",
              "dynamodb:ListTables",
              "dynamodb:Query",
              "dynamodb:Scan",
              "dynamodb:DescribeReservedCapacity",
              "dynamodb:DescribeReservedCapacityOfferings",
              "dynamodb:ListTagsOfResource",
              "dynamodb:DescribeTimeToLive",
              "dynamodb:DescribeLimits"
          ],
          "Effect": "Allow",
          "Resource": "*"
        }
      ]
    })
