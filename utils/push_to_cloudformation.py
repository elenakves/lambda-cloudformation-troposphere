import os
import boto3
import boto3.s3.transfer as tr
from configobj import ConfigObj

lambda_config = ConfigObj(os.path.join('conf', 'variables.conf'))

def s3_upload(file, bucket):
    client = boto3.client('s3', 'eu-west-1')
    transfer = tr.S3Transfer(client)
    transfer.upload_file(file, bucket, file)


def main():

    stack = lambda_config['GLOBAL']['stack']

    stack_template = 'output/'+lambda_config['GLOBAL']['output_file']

    bucket = 'cf-templates-1c7mezceyo7yt-eu-west-1'

    region = lambda_config['GLOBAL']['region']

    url = 'https://s3-{0}.amazonaws.com/{1}/{2}'.format(region,
                                                        bucket,
                                                        stack_template)
    s3_upload(stack_template, bucket)

    cf = boto3.client('cloudformation', region_name=region)
    cf.create_stack(
        StackName=stack,
        TemplateURL=url,
        Capabilities=['CAPABILITY_IAM']
    )

if __name__ == "__main__":
    main()
