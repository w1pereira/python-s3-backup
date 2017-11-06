"""This script zip folders and files (according to an regex pattern)
    and upload to Amazon S3 service."""

import os
import re
import zipfile
import json
import time
import boto3

# Configuration file
with open('config.json') as json_data_file:
    CONFIG = json.load(json_data_file)

def zipd(directory, path):
    """Zip entire directory."""
    path = ('' if path == '.' else path) + directory
    filename = path + '.zip'
    zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()
    return filename

def backupd(path, pattern, prefix=''):
    """Backup folders based on given path, regex pattern and a optional prefix
       for filename (backup file)."""
    for directories in os.walk(path, topdown=True):
        for directory in directories[1]:
            folder_name = re.search(pattern, directory)
            if folder_name is not None:
                backupfile = zipd(directory, path)
                upload(backupfile, prefix + directory + '.zip')
                # Delete backup file after uploaded (zip)
                os.remove(backupfile)

def backupf(path, pattern, backup_filename):
    """Backup files based on regex pattern"""
    backupfile = ('' if path == '.' else path) + backup_filename + '.zip'
    zipf = zipfile.ZipFile(backupfile, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path, topdown=True):
        for file in files:
            filename = re.search(pattern, file)
            if filename is not None:
                zipf.write(os.path.join(root, file))
    zipf.close()
    upload(backupfile, backup_filename + '.zip')
    # Delete backup file after uploaded (zip)
    os.remove(backupfile)

def upload(path, key):
    """Upload file to Amazon S3"""
    s3_client = boto3.resource(
        's3',
        aws_access_key_id=CONFIG['aws']['s3']['access-key'],
        aws_secret_access_key=CONFIG['aws']['s3']['secret-access-key']
    )
    s3_client.meta.client.upload_file(path, CONFIG['aws']['s3']['bucket'],
                                      time.strftime("%Y/%m/%d/") + key)

# Folder name examples: Backup_Relatorios_2110_2017_00_00,
# Backup_Imagens_2110_2017_00_00. File Examples: Backup_BACKUPLOG_0611_2017_00_00.log
# backupd('.', '_(.*)_(\\d{2})(\\d{2})_(\\d{4})_(\\d{2})_(\\d{2})')
# backupf('.', '_(.*)_' + time.strftime("%d%m") + '_(\\d{4})_(\\d{2})_(\\d{2})',
#         'BACKUPLOG_' + time.strftime("%d%m_%Y"))
