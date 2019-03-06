"""
REFERENCE FUNCTIONS ONLY - DO NOT RUN MANUALLY
"""
import zipfile
import os
import boto3
import boto3.s3.transfer as tr
import shutil
from configobj import ConfigObj

lambda_config = ConfigObj(os.path.join('conf', 'variables.conf'))
bucket_name = lambda_config['GLOBAL']['BUCKETNAME']
package_loc = lambda_config['GLOBAL']['deployment_package_location']

def zip_and_load(file, load_packages='N'):
    """
    create deployment package and send it to s3
    """
    os.chdir('lambda')
    basename = os.path.basename(file)

    file_out = os.path.splitext(basename)[0] + '.zip'
    file_base = os.path.splitext(basename)[0]

    if load_packages == 'Y':
        arc = shutil.make_archive(base_name=file_base,
                                  format='zip',
                                  root_dir=package_loc)
        # print(arc)

    with zipfile.ZipFile(file_out, mode='a') as z:
        z.write(basename)

    client = boto3.client('s3', 'eu-west-1')
    transfer = tr.S3Transfer(client)
    transfer.upload_file(file_out,
                         bucket_name,
                         os.path.basename(file_out))
    os.remove(file_out)
    os.chdir('..')
