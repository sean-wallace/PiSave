#!/usr/bin/python
import fnmatch, os, dropbox, time
from dropbox.files import WriteMode

dbx = dropbox.Dropbox('API_KEY')

overwrite = WriteMode('overwrite', None)

CHUNK_SIZE = 4 * 1024 * 1024

for root, dirs, files in os.walk(r'/home/pi/RetroPie/roms'):
    for saves in files:
        file_path = root + '/' + saves
        dest_path = root + '/' + saves
        if saves.endswith(('.state', '.srm')):                
            f = open(file_path)
            file_size = os.path.getsize(file_path)
            if file_size <= CHUNK_SIZE:
			
                print dbx.files_upload(f.read(), dest_path, overwrite)
                
            else:

                upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
                cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                                           offset=f.tell())
                commit = dropbox.files.CommitInfo(path=dest_path)

                while f.tell() < file_size:
                    if ((file_size - f.tell()) <= CHUNK_SIZE):
                        print dbx.files_upload_session_finish(f.read(CHUNK_SIZE),
                                                        cursor,
                                                        commit)
                    else:
                        dbx.files_upload_session_append(f.read(CHUNK_SIZE),
                                                        cursor.session_id,
                                                        cursor.offset)
                        cursor.offset = f.tell()
            f.close()
            time.sleep(2)