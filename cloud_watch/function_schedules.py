"""
Python Script       : cloud_watch/function_schedules.py

This script creates the CloudWatch Events that will be used to schedule Lambda functions.
Within each function definition we create a Target object. These objects need
to be imported here and added to the correct scheduling definition.

"""
# REQUIRED MODULE IMPORTS
from troposphere.events import Rule

# IMPORT FUNCTION TARGETS
from templates import lambda_template

[function, target] = lambda_template.lambda_configuration('url_string_check')
url_string_check_target = target
print(url_string_check_target)

# initiate empty list to add targets
resources = []

"""
SCHEDULE DEFINITIONS
"""
url_check_schedule = Rule(
    'UrlCheckSchedule',
    Description='testing',
    Name='url-check-schedule',
    ScheduleExpression="cron(0/5 * * * ? *)",
    Targets=[
        url_string_check_target
    ])
resources.append(url_check_schedule)

