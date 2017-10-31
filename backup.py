"""This script zip folders (according to an regex pattern)
    and upload to Amazon S3 service."""

import os
import re
import zipfile

# PATH = '.'

def zipdir(path, ziph):
    """Zip entire directory."""
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def backup(path, pattern):
    """Backup folders based on given path and regex pattern."""
    for directories in os.walk(path):
        for directory in directories[1]:
            folder_name = re.search(pattern, directory)
            if folder_name is not None:
                filename = ('' if path == '.' else path) + directory + '.zip'
                zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
                zipdir(directory, zipf)
                zipf.close()
        break

# Folder name examples: Backup_Relatorios_2110_2017_00_00,
# Backup_Imagens_2110_2017_00_00
# backup(PATH, '_(.*)_(\\d{2})(\\d{2})_(\\d{4})_(\\d{2})_(\\d{2})')
