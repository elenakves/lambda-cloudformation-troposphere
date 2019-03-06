"""
Python Script       : templates/lambda_template.py

This script creates templates for Lambda functions. It uses variables.conf file, where Lambda functions are described.
It takes one parameter 'name' which is the function name that should be passed as argument, when calling from create_and_deploy_cfn_template.py
It returns list two values: resources and target
"""
# REQUIRED MODULE IMPORTS
import os
import sys
import troposphere.awslambda as lmb
from troposphere import GetAtt
from troposphere.iam import Role
from troposphere.events import Target
from configobj import ConfigObj

import utils.load_functions_to_s3 as s3
import iam_roles.lambda_policies as iam

lambda_config = ConfigObj(os.path.join('conf', 'variables.conf'))

# create json object for lambda function
def lambda_configuration(name):
    resources = []
    
    """
    define variables
    """
    select_function = name
    print("passing function name to configuration: {}".format(name))
    
    bucket_name = lambda_config['GLOBAL']['BUCKETNAME']
    dynamodb_table = lambda_config['DynamoDB']['table_name']
    source_file_name = lambda_config['Lambda']['functions'][select_function]['source_file_name']
    title = lambda_config['Lambda']['functions'][select_function]['title']
    load_packages = lambda_config['Lambda']['functions'][select_function]['load_packages']
    
    assigned_roles = [iam.allow_lambda_execute,        # REQUIRED TO ENABLE LOGGING
                      iam.allow_dynamodb_action]
    
    function_name = lambda_config['Lambda']['functions'][select_function]['function_name']
    function_description = lambda_config['Lambda']['functions'][select_function]['function_description']
    function_to_run = lambda_config['Lambda']['functions'][select_function]['function_to_run']
    memory_size = int(lambda_config['Lambda']['functions'][select_function]['memory_size'])
    timeout = lambda_config['Lambda']['functions'][select_function]['timeout']
    
    environment_var = lmb.Environment(
       Variables={"SITE": "https://aws.amazon.com/console/",
                  "EXPECTED":"AWS"}
       )
    
    if memory_size > 1536:
        sys.exit("Memory Size too large")
    if memory_size < 128:
        sys.exit("Memory Size too small")
    if memory_size % 64 != 0:
        sys.exit("Memory Size not a multiple of 64")
    
    source = 'lambda/{0}'.format(source_file_name)
    file_name_only = os.path.splitext(os.path.basename(source))[0]
    zip_file = file_name_only + '.zip'
    function_handler = file_name_only + '.' + function_to_run
    
    role_title = '{0}Role'.format(title)
    code_title = '{0}Code'.format(title)
    function_title = '{0}Function'.format(title)
    permission_title = '{0}Permission'.format(title)
    target_id = '{0}Target'.format(title)
    
    # Copy the source file into the S3 Bucket
    s3.zip_and_load(source, load_packages=load_packages)
    
    role = Role(
        role_title,
        AssumeRolePolicyDocument=iam.lambda_assume_role,
        Policies=assigned_roles
    )
    resources.append(role)
    
    code = lmb.Code(
        code_title,
        S3Bucket=bucket_name,
        S3Key=zip_file
    )
    
    function = lmb.Function(
       function_title,
       FunctionName=function_name,
       Description=function_description,
       Code=code,
       Handler=function_handler,
       MemorySize=memory_size,
       Role=GetAtt(role_title, "Arn"),
       Environment=environment_var,
       Runtime='python3.6',
       Timeout=timeout
    )

    resources.append(function)
    
    permission = lmb.Permission(
        permission_title,
        FunctionName=function_name,
        Action="lambda:InvokeFunction",
        Principal="events.amazonaws.com",
        DependsOn=function_title
    )
    resources.append(permission)
    print("type resources is: {} ".format(type(resources)))
    
    target = Target(
        Arn=GetAtt(function, "Arn"),
        Id=target_id
    )
    print("type target is: {}".format(target))
    """we need to return both: list of resources and target. The last will be used for CW rule """
    return [resources, target]

