#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.docx2txt`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Docx Conversion(docs -> txt) plugin
"""
# Authors
# ===========
#
# * Irene Cho
#
# --------
#
#  * [2021/06/22]
#     - starting

################################################################################
import os
import sys
import pypandoc
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
@func_log
def doc2txt(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        fn = argspec.filename
        if not os.path.exists(fn):
            raise IOError('Cannot read doc file "%s"' % fn)
        if not argspec.output:
            argspec.output = fn[0:-5] + ".txt"
        pypandoc.convert_file(fn, 'plain',
                              outputfile=argspec.output)
        print(argspec.output, end='')
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
            owner='ARGOS-LABS',
            group='2',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Doc2TXT',
            icon_path=get_icon_path(__file__),
            description='Converting from word file to text file',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('filename', display_name='Docx File',
                          input_method='fileread', help='Select a word file')
        mcxt.add_argument('--output', display_name='Output Filepath',
                          input_method='filewrite',
                          help='Specify an absolute file path to save the output')
        argspec = mcxt.parse_args(args)
        return doc2txt(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
