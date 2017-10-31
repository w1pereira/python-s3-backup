"""This script zip backup folders (according to an regex pattern)
    and send it to Amazon S3 service."""

import os
import re
import zipfile

PATH = '.'

def zipdir(path, ziph):
    """Zip entire directory."""
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

for directories in os.walk(PATH):
    for d in directories[1]:
        # Folder name examples: Backup_Relatorios_2110_2017_00_00, Backup_Imagens_2110_2017_00_00
        folder_name = re.search('_(.*)_(\\d{2})(\\d{2})_(\\d{4})_(\\d{2})_(\\d{2})', d)
        if folder_name is not None:
            filename = ('' if PATH == '.' else PATH) + d + '.zip'
            zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
            zipdir(d, zipf)
            zipf.close()
    break
