#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.chardet`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for converting encoding
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/06]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/03/26]
#     - starting

################################################################################
import os
import sys
import csv
import chardet
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
@func_log
def detect_encoding(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        if not os.path.exists(argspec.file):
            raise IOError(f'Cannot find file "{argspec.file}"')
        c = csv.writer(sys.stdout, lineterminator='\n')
        h = ('language', 'encoding', 'confidence')
        c.writerow(h)
        with open(argspec.file, 'rb') as ifp:
            dr = chardet.detect(ifp.read())
            c.writerow((dr[h[0]], dr[h[1]], dr[h[2]]))
        return 0
    except Exception as e:
        msg = 'argoslabs.data.chardet Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
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
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Detect CharSet',
        icon_path=get_icon_path(__file__),
        description='Detect Charecter Set',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('file',
                          display_name='File',
                          input_method='fileread',
                          help='File name to detect file characterset')
        argspec = mcxt.parse_args(args)
        return detect_encoding(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
