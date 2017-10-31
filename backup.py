"""This script zip folders (according to an regex pattern)
    and upload to Amazon S3 service."""

import os
import re
import zipfile
import json
import boto3

# Configuration file
with open('config.json') as json_data_file:
    CONFIG = json.load(json_data_file)

def zipdir(directory, path):
    """Zip entire directory."""
    filename = ('' if path == '.' else path) + directory + '.zip'
    zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()
    return filename

def backup(path, pattern):
    """Backup folders based on given path and regex pattern."""
    for directories in os.walk(path, topdown=True):
        for directory in directories[1]:
            folder_name = re.search(pattern, directory)
            if folder_name is not None:
                backupfile = zipdir(directory, path)
                upload(backupfile, directory + '.zip')

def upload(path, key):
    """Upload file to Amazon S3"""
    s3_client = boto3.resource(
        's3',
        aws_access_key_id=CONFIG['aws']['s3']['access-key'],
        aws_secret_access_key=CONFIG['aws']['s3']['secret-access-key']
    )
    s3_client.meta.client.upload_file(path, CONFIG['aws']['s3']['bucket'], key)

# Folder name examples: Backup_Relatorios_2110_2017_00_00,
# Backup_Imagens_2110_2017_00_00
# backup('.', '_(.*)_(\\d{2})(\\d{2})_(\\d{4})_(\\d{2})_(\\d{2})')
