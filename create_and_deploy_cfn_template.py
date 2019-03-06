"""
Python Script       : create_and_deploy_cfn_template.py
This function outputs .json template to create/update cfn stack
"""
import os
import sys

from configobj import ConfigObj

import templates.dynamodb as dynamodb
from templates import lambda_template
from utils import push_to_cloudformation as pcf
from cloud_watch.function_schedules import resources as fsr

template = dynamodb.t
"""it's <troposphere.Template object at 0x000002548A8026A0>  """
"""now we need to add Lambdas to the template"""

config_file = ConfigObj(os.path.join('conf', 'variables.conf'))


def add_lambda_to_cfn_template(name):
    """"this function get both objects returned by lambda_template.py. For the list of resources this function calls add_resources method
     to add resources to cfn template"""
    [resources, target] = lambda_template.lambda_configuration(name)
    for_template = [resources]
    """we dont need target here, we will use it later for CW schedule add_cw_to_cfn_template(schedule_list)"""
    for r in for_template:
        template.add_resource(r)


def add_cw_to_cfn_template(schedule_list):
    for s in schedule_list:
        template.add_resource(s)


def main(*args):
    print("Creating template")

    template.add_version(config_file['GLOBAL']['template_version'])
    template.add_description(config_file['GLOBAL']['template_description'])

    add_lambda_to_cfn_template('url_string_check')

    add_cw_to_cfn_template(fsr)

    f = open(os.path.join('output', '{0}'.format(config_file['GLOBAL']['output_file'])), 'w')
    f.write(template.to_json())
    f.close()


if __name__ == "__main__":
    main(sys.argv)
    pcf.main()
