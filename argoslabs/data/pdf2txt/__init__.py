#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.pdf2txt`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS PDF Conversion(pdf -> txt) plugin
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
import PyPDF2
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
@func_log
def pdf2doc(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        fn = argspec.filename
        if not os.path.exists(fn):
            raise IOError('Cannot read pdf file "%s"' % fn)
        pdfFileObj = open(fn, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        x = pdfReader.numPages
        if not argspec.output:
            argspec.output = fn[0:-4] + ".txt"
        with open(argspec.output, 'w') as f:
            for i in range(x):
                pageObj = pdfReader.getPage(i)
                f.write(pageObj.extractText())
        pdfFileObj.close()
        f.close()
        print(os.path.abspath(argspec.output), end='')
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
            display_name='PDF2TXT',
            icon_path=get_icon_path(__file__),
            description='Converting from pdf file to text file',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('filename', display_name='PDF File',
                          input_method='fileread', help = 'Select a pdf file')
        mcxt.add_argument('--output', display_name='Output Filepath',
                          input_method='filewrite',
                          help = 'Specify an absolute file path to save the output')
        argspec = mcxt.parse_args(args)
        return pdf2doc(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
