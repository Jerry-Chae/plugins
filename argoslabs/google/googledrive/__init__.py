"""
====================================
 :mod:`argoslabs.google.googledrive`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS managing google drive
"""
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2020/06/15]
#     - Remove create a token.pickle operation
#
#  * [2020/06/11]
#     - starting

################################################################################
from __future__ import print_function
import sys
import pickle
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import warnings


################################################################################
class Googledrive(object):
    # ==========================================================================
    OP_TYPE = ['Create a Folder', 'Upload a File',
               'Download a File',
               'Recently Modified', 'Search', 'Share File/Folder']
    USER_TYPE = ['user', 'group', 'domain', 'anyone']
    ROLE_TYPE = ['reader', 'writer', 'commenter']
    FILE_TYPE = ['File in Google Drive', 'G Suite Files']

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.service = None

    # ==========================================================================
    def read_file(self):
        if self.argspec.token:
            k = self.argspec.token
            if '\n' in k:
                k = k.strip('\n')
            with open(k, 'rb') as token:
                creds = pickle.load(token)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
        self.service = build('drive', 'v3', credentials=creds)
        return self.service

    # ==========================================================================
    def create_folder(self, folderename):
        file_metadata = {
            'name': folderename,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        results = self.service.files().create(body=file_metadata,
                                              fields='id').execute()
        print(results.get('id').strip(), end="")
        return results.get('id')

    # ==========================================================================
    def upload_file(self, filename, folder_id=None):
        file_metadata = {
            'name': os.path.basename(filename),
        }
        if folder_id:
            file_metadata['parents'] = [folder_id.strip()]
        media = MediaFileUpload(filename,
                                resumable=True)
        file = self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
        print(file.get('id').strip(), end="")

    # ==========================================================================
    def download_file(self, fileid, filetype, filepath):
        res = self.service.files().get(
            fileId=fileid).execute()
        if filetype == 'File in Google Drive':
            request = self.service.files().get_media(fileId=fileid)
        elif filetype == 'G Suite Files':
            request = self.service.files(). \
                export_media(fileId=fileid, mimeType=self.argspec.mimeType)
        filepath = os.path.join(filepath, res['name'])
        fh = open(filepath, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        print(os.path.abspath(filepath), end="")

    # https://developers.google.com/drive/api/v3/ref-export-formats

    # ==========================================================================
    def filelist(self):
        query=None
        if self.argspec.folderid:
            query=f"parents in '{self.argspec.folderid}'"
        results = self.service.files().list(pageSize=self.argspec.pagesize,
                                            fields="nextPageToken, "
                                                   "files(id, name)",
                                            q=query).execute()

        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('name,id')
            for item in items:
                print(u'{0},{1}'.format(item['name'], item['id']))

    # ==========================================================================
    def search(self, query):
        page_token = None
        if self.argspec.folderid:
            folder_query = f"parents in '{self.argspec.folderid}'"
            query = query + ' and ' + folder_query
        while True:
            response = self.service.files().list(q=query,
                                                 fields='nextPageToken, '
                                                        'files(id, name)',
                                                 pageToken=page_token).execute()
            if not response.get('files',[]):
                print('No files found.')
            else:
                print('name,id')
                for file in response.get('files', []):
                    print(u'{0},{1}'.format(file.get('name'), file.get('id')))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    # ==========================================================================
    def sharefiles(self, usertype, role, file, address=None):
        def callback(request_id, response, Exception):
            if Exception:
                raise IOError(Exception)
            else:
                print(file, end="")

        batch = self.service.new_batch_http_request(callback=callback)
        if usertype == 'user' or usertype == 'group':
            permission = {
                'type': usertype,
                'role': role,
                'emailAddress': address
            }
        elif usertype == 'domain':
            permission = {
                'type': usertype,
                'role': role,
                'domain': address
            }
        else:
            permission = {
                'type': usertype,
                'role': role,
            }
        batch.add(self.service.permissions().create(
            fileId=file.strip(),
            body=permission,
            fields='id',
        ))
        batch.execute()

    # =========================================================================
    def do(self, op):
        if op == 'Create a Folder':
            self.create_folder(self.argspec.foldername)
        elif op == 'Upload a File':
            self.upload_file(self.argspec.filepath, self.argspec.folderid)
        elif op == 'Download a File':
            self.download_file(self.argspec.fileid, self.argspec.filetype,
                               self.argspec.filepath)
        elif op == 'Recently Modified':
            self.filelist()
        elif op == 'Search':
            self.search(self.argspec.query)
        elif op == 'Share File/Folder':
            if self.argspec.fileid:
                file = self.argspec.fileid
            elif self.argspec.folderid:
                file = self.argspec.folderid
            else:
                raise IOError('Cannot find any file to share')
            self.sharefiles(self.argspec.usertype, self.argspec.role, file,
                            self.argspec.address)


################################################################################
@func_log
def reg_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        warnings.simplefilter("ignore", ResourceWarning)
        res = Googledrive(argspec)
        res.read_file()
        res.do(argspec.op)
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS-DEMO',
            group='2',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Google Drive',
            icon_path=get_icon_path(__file__),
            description='Managing files in Google Drive',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='Function type',
                          choices=Googledrive.OP_TYPE,
                          help='Type of operation')
        mcxt.add_argument('token', display_name='Token.Pickle',
                          help='Token file', show_default=True,
                          input_method='fileread')
        # ######################################## for app dependent options
        mcxt.add_argument('--pagesize', display_name='# of file/folder',
                          help='Pagesize of file list', default=10, type=int)
        mcxt.add_argument('--foldername', display_name='Folder Name',
                          help='Create a new folder name')
        mcxt.add_argument('--filepath', display_name='Filepath',
                          help='Absolute filepath', input_method='fileread')
        mcxt.add_argument('--fileid', display_name='File ID',
                          help='File Id in Google Drive')
        mcxt.add_argument('--filetype', display_name='File Type',
                          help='Type of downloading files',
                          choices=Googledrive.FILE_TYPE)
        mcxt.add_argument('--mimeType', display_name='MimeType',
                          help='G suite documents and corresponding export '
                               'MIME types')
        mcxt.add_argument('--folderid', display_name='Folder ID',
                          help='File Id in Google Drive')
        mcxt.add_argument('--query', display_name='Search Query',
                          help='queries to find a specific file in drive',
                          default="fullText contains 'hello world'")
        mcxt.add_argument('--usertype', display_name='User Type',
                          help='Type of user who will receive permission',
                          choices=Googledrive.USER_TYPE)
        mcxt.add_argument('--role', display_name='Role Type',
                          help='Type of role', choices=Googledrive.ROLE_TYPE)
        mcxt.add_argument('--address',
                          display_name='Address',
                          help='Address to give the permission')
        argspec = mcxt.parse_args(args)
        return reg_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
