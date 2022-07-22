#!/usr/bin/env python
# coding=utf8


"""
====================================
 :mod:`argoslabs.storage.boxii`
====================================
.. moduleauthor:: Arun Kumar <ak080495@gmail.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS-LABS RPA Boxsdk plugin module

"""
# Authors Irene Cho
# ===========
#
# * Arun Kumar ,
#
# Change Log
# --------
#
#  * [2022/07/18]
#     - file list
#  * [2022/07/19]
#     - conf files
#  * [2022/07/20]
#     - generate token
#  * [2022/07/20]
#     - generate token show fix


################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path

from io import StringIO
from boxsdk import OAuth2, Client
from boxsdk.exception import BoxAPIException

from alabslib.selenium import PySelenium
# from alabs.common.util.vvlogger import get_logger
# from tempfile import gettempdir
import logging

################################################################################
class sel(PySelenium):
    # ==========================================================================
    def __init__(self, url, user_id, pwd, **kwargs):
        kwargs['url'] = url
        PySelenium.__init__(self, **kwargs)
        self.user_id = user_id
        self.pwd = pwd

    # ==========================================================================
    def start(self):
        e = self.get_by_xpath(
            '/html/body/div[3]/div/div[1]/div[2]/div/div[1]/form/div[1]/div[1]/div[1]/input')
        e.send_keys(self.user_id)
        e = self.get_by_xpath(
            '/html/body/div[3]/div/div[1]/div[2]/div/div[1]/form/div[1]/div[1]/div[2]/input')
        e.send_keys(self.pwd)
        e = self.get_by_xpath(
            '/html/body/div[3]/div/div[1]/div[2]/div/div[1]/form/div[1]/div[2]/input')
        self.safe_click(e)
        self.implicitly_wait()
        e = self.get_by_xpath(
            '/html/body/div[3]/div/div/div/form/div/div[1]/button')
        self.safe_click(e)
        self.implicitly_wait()
        cur = self.driver.current_url
        code = cur.split('code=')[1]
        return code

################################################################################
@func_log
def helloworld(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        if argspec.token:
            oauth = OAuth2(
                client_id=argspec.cid, client_secret=argspec.csecret,
                access_token=argspec.token
            )
        else:
            oauth = OAuth2(client_id=argspec.cid, client_secret=argspec.csecret)
        client = Client(oauth)

        if argspec.op == 'Get Access Token':
            auth_url = oauth.get_authorization_url(
                argspec.redirect_uri)[0]

            def do_start(**kwargs):
                with sel(
                        kwargs['url'],
                        kwargs['user_id'],
                        kwargs['pwd'],
                        headless=kwargs.get('headless', False),
                        browser=kwargs.get('browser', 'Chrome'),
                        width=int(kwargs.get('width', '1200')),
                        height=int(kwargs.get('height', '800')),
                        logger=kwargs['logger']) as ws:
                    return ws.start()

            # log_f = os.path.join(gettempdir(), "a.log")
            # print(log_f,"iasgduiashfil")
            # logger = get_logger(log_f, logsize=1024 * 1024 * 10)
            # print(logger)

            logger = logging.getLogger('argoslabs.boxii.boxII')
            _kwargs = {
                'browser': 'Chrome',
                'url': auth_url,
                'user_id': argspec.user_id,
                'pwd': argspec.pwd,
                'headless': True,
                'logger': logger,
            }
            # print(_kwargs)

            code = do_start(**_kwargs)
            access_token = oauth.authenticate(code)[0]
            print(str(access_token), end='')

        elif argspec.op == 'File/Folder Lists':
            outst = StringIO()
            outst.write('type,id,name')
            outst.write('\n')
            items = client.folder(argspec.folderid).get_items()
            for i in items:
                outst.write(i.type + ',' + str(i.id) + ',' + i.name)
                outst.write('\n')
            print(outst.getvalue(), end='')


        elif argspec.op == 'Upload Files':

            outst = StringIO()
            outst.write('name,id')
            outst.write('\n')
            cnt = 0
            err = ''
            for ent in argspec.files:
                try:
                    _item = client.folder(argspec.folderid).upload(file_path=ent)
                    # print(abc,"skjdfgjfhbjkl")
                    # print(abc.name, "skjdfgjfhbjkl")
                    # print(abc.id, "skjdfgjfhbjkl")
                    outst.write(_item.name+','+str(_item.id))
                    outst.write('\n')
                    cnt += 1
                except BoxAPIException as msg:
                    err = str(msg)
                    pass
            if cnt==0:
                msg = str(err)
                mcxt.logger.error(msg)
                sys.stderr.write('%s%s' % (msg, os.linesep))
                return 1
            else:
                # print(f'Successfully uploaded {cnt} files', end='')
                print(outst.getvalue(), end='')


        elif argspec.op == 'Download Files/Folder':
            items = []
            try:
                if argspec.folderid is None and argspec.fileid is None:
                    msg = "Folder ID or File ID required"
                    mcxt.logger.error(msg)
                    sys.stderr.write('%s%s' % (msg, os.linesep))
                    return 1

                if argspec.output is None:

                    msg = "Output Path required"
                    mcxt.logger.error(msg)
                    sys.stderr.write('%s%s' % (msg, os.linesep))
                    return 1

                if argspec.folderid:
                    items += client.folder(argspec.folderid).get_items()

                if argspec.fileid:
                    for id in argspec.fileid:
                        items.append(client.file(id).get())
                for ent in items:
                    outst = StringIO()

                    if ent.type == 'folder':
                        pass
                    else:
                        location = os.path.join(argspec.output, ent.name)
                        i=1
                        def create_dir(cf_ent, _location):
                            if not os.path.exists(_location):
                                return _location
                            cf_ent += 1
                            return create_dir(cf_ent,_location.replace("("+str(cf_ent-1)+")","("+str(cf_ent)+")"))

                        if os.path.exists(location) == True:
                            base = os.path.basename(location)
                            _a = os.path.splitext(base)[0]
                            tem_location = os.path.join(argspec.output, os.path.splitext(base)[0]+ "("+str(i)+")"+os.path.splitext(base)[1])
                            location = create_dir(i,tem_location)
                        output_file = open(location, 'wb')
                        client.file(ent.id).download_to(output_file)
                        outst.write(location)
                        outst.write('\n')
                        print(outst.getvalue(), end='')
            except Exception as err:
                msg = str(err)
                mcxt.logger.error(msg)
                sys.stderr.write('%s%s' % (msg, os.linesep))
                return 99



        mcxt.logger.info('>>>end...')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='8',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Box II',
        icon_path=get_icon_path(__file__),
        description='Box SDK Module',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='OP Type', help='operation types',
                          choices=['Get Access Token', 'File/Folder Lists',
                                   'Upload Files',
                                   'Download Files/Folder'])
        # ----------------------------------------------------------------------
        mcxt.add_argument('csecret', display_name='Client Secret',
                          help='Client Secret',
                          input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('cid', display_name='Client ID', help='Client ID')
        # ##################################### for app optional parameters
        mcxt.add_argument('--token', display_name='Token', help='Token',
                          input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--redirect_uri', display_name='Redirect URI',
                          help='Redirect URI')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--user_id', display_name='User ID',
                          help='user id')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--pwd', display_name='Password',
                          help='Password', input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--files', display_name='Files to Upload',
                          input_method='fileread', action='append',
                          help='Files to upload to BOX')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--folderid', display_name='Folder ID',
                          help='Folder ID from BOX')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--fileid', display_name='File ID', action='append',
                          help='File ID from BOX')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--output', display_name='Output Path',
                          input_method='folderwrite',
                          help='An absolute filepath to save a file')
        argspec = mcxt.parse_args(args)
        return helloworld(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
