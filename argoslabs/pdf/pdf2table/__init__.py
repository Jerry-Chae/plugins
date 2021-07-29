#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.pdf2txt`
====================================
.. moduleauthor:: Kyobong An <akb0930e@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS PDF Conversion(pdf -> txt) plugin
"""
# Authors
# ===========
#
# * Kyobong An
#
# --------
#
#  * [2021/07/28]
#     - starting

################################################################################
import os
import sys
import pdfplumber
# import pandas
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class TableError(Exception):
    pass


################################################################################
@func_log
def pdf2doc(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    if argspec.table:
        pdffile = argspec.table
    else:
        pdffile = argspec.text
    try:
        text = str()
        with pdfplumber.open(pdffile) as pdf, open(argspec.output, 'w') as txt:
            pages = pdf.pages
            if argspec.text:
                for page in pages:
                    text += page.extract_text()

                txt.write(text)
            else:
                count = 0
                for page in pages:
                    tables = page.extract_tables(table_settings=
                                                 {"vertical_strategy": argspec.vertical,
                                                  "horizontal_strategy": argspec.horizontal,
                                                  })
                    for table in tables:
                        for r_table in table:
                            txt.write(',\t'.join(i if i else '' for i in r_table) + '\n')
                            count += 1
                            # print(','.join(r_table))
                        txt.write('\n'*4)
                if count == 0:
                    msg = ('The table is not included in "%s"' % os.path.basename(argspec.table))
                    raise TableError(msg)
            pdf.close()
            txt.close()

        print(os.path.abspath(argspec.output), end='')
        return 0
    except TableError as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 9
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
            display_name='PDF2Table',
            icon_path=get_icon_path(__file__),
            description='Converting from pdf file to text file',
    ) as mcxt:
        # ##################################### for app dependent options
        # ----------------------------------------------------------------------
        mcxt.add_argument('--table',
                          display_name='Table', show_default=True,
                          input_method='fileread',
                          input_group='radio=PDF File;default',
                          help='Select a pdf file for table')
        mcxt.add_argument('--text',
                          display_name='Text', show_default=True,
                          input_method='fileread',
                          input_group='radio=PDF File',
                          help='Select a pdf file for text')
        mcxt.add_argument('--output', display_name='Output Filepath', show_default=True,
                          input_method='filewrite',
                          help='Specify an absolute file path to save the output')
        mcxt.add_argument('--vertical',
                          display_name='Vertical strategy', default="lines",
                          choices=["lines", "lines_strict", "text", "explicit"],
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--horizontal',
                          display_name='Horizontal strategy', default="lines",
                          choices=["lines", "lines_strict", "text", "explicit"],
                          input_group='Table option',
                          help='for more information refer to the help page')
        argspec = mcxt.parse_args(args)
        return pdf2doc(mcxt, argspec)
        # ##################################### for app dependent parameters


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
